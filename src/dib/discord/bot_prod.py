import os

# from groq import Groq
import discord
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.groq import Groq
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from icecream import ic


load_dotenv()


def set_client():

    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API")
    )

    llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API"))

    embed_model = CohereEmbedding(
        cohere_api_key=os.getenv("COHERE_API_KEY"),
        model_name="embed-english-v3.0",
        input_type="search_query",
    )

    Settings.llm = llm
    Settings.embed_model = embed_model

    vector_store = QdrantVectorStore(
        client=qdrant_client, collection_name="RAG_chunks"
    )

    return vector_store, llm, embed_model


vector_store, llm, embed_model = set_client()

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

cohere_rerank = CohereRerank(api_key=os.getenv("COHERE_API_KEY"), top_n=2)


query_engine = index.as_query_engine(
    similarity_top_k=10, node_postprocessors=[cohere_rerank]
)

chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine, verbose=True, llm=llm, embed_model=embed_model
)

# Starting Discord section
intents = discord.Intents.default()
intents.message_content = True

# Set Discord client
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")


@client.event
async def on_message(message):
    print(message.author)
    if message.author == client.user:  # no action if message is from chatbot
        return
    if message.content.startswith("$bot"):  # bot call
        if type(message.channel) == discord.channel.TextChannel:
            async with message.channel.typing():
                proc_message = message.content.split("$bot ")[1]
                if (
                    len(proc_message) > 100
                ):  # Thread title can't be more than 100 characters
                    message.channel = await message.create_thread(
                        name=proc_message[:90]
                    )
                else:
                    message.channel = await message.create_thread(
                        name=proc_message
                    )

                ic(type(message.channel))

                chat_engine = CondenseQuestionChatEngine.from_defaults(
                    query_engine=query_engine,
                    verbose=True,
                    llm=llm,
                    embed_model=embed_model,
                )  # main chat engine

                response = chat_engine.chat(proc_message)
                sources = response.sources
                final_response = response.response
                if (
                    len(final_response) > 1900
                ):  # Discord max length for response is 2000 characters
                    final_response = final_response[:1900]
                ic(final_response)
                ic(sources)
                await message.channel.send(f"{final_response}")  # Send message

        elif type(message.channel) == discord.threads.Thread:

            messages = [
                message
                async for message in message.channel.history(
                    limit=25, oldest_first=True
                )
            ]  # Get Message history from thread

            full_mssg = []
            for idx, val in enumerate(
                messages
            ):  # format message history for chat engine
                if str(val.author) != "LilJohn#0825":
                    if val.content.startswith("$bot "):
                        proc_message = val.content.split("$bot ")[1]
                        us_mssg = ChatMessage(
                            role=MessageRole.USER, content=proc_message
                        )
                        full_mssg.append(us_mssg)
                    else:
                        pass  # question whether we should add non $bot messages to llm mssg history
                else:
                    as_mssg = ChatMessage(
                        role=MessageRole.ASSISTANT, content=val.content
                    )

                    full_mssg.append(as_mssg)

            full_mssg[0] = ChatMessage(
                role=MessageRole.USER,
                content=message.channel.starter_message.content.split("$bot ")[
                    1
                ],
            )  # remove the bot call from message
            full_mssg = full_mssg[
                :-1
            ]  # remove the last message because we're going to add it to the chat engine below
            print(full_mssg)

            chat_engine = CondenseQuestionChatEngine.from_defaults(
                query_engine=query_engine,
                verbose=True,
                llm=llm,
                embed_model=embed_model,
                chat_history=full_mssg,
            )  # send itttt

            response = chat_engine.chat(proc_message).response

            if len(response) > 1900:  # Discord 2000 character limit
                response = response[:1900]
            print(response)
            await message.channel.send(f"{response}")


client.run(os.getenv("DISCORD_TOKEN"))
