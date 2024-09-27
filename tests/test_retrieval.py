from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.cohere import CohereEmbedding
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
from llama_index.llms.anyscale import Anyscale

load_dotenv()


qdrant_client = QdrantClient(url = os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API"))

llm = Anyscale(api_key = os.getenv("ANYSCALE_API_KEY"))

embed_model = CohereEmbedding(cohere_api_key = os.getenv("COHERE_API_KEY"), model_name = "embed-english-v3.0", input_type="search_query")

Settings.llm = llm
Settings.embed_model = embed_model


vector_store = QdrantVectorStore(client = qdrant_client, collection_name = "RAG_chunks")

index = VectorStoreIndex.from_vector_store(vector_store = vector_store)

query_engine = index.as_query_engine()

response = query_engine.query("Explain linear regression.")



print(response)

print(f"Source Nodes: \n {response.source_nodes}")
