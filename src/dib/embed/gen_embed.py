import json
import os
import typing

import openai
from dotenv import load_dotenv
from llama_index.core import (Document, Settings, StorageContext,
                              VectorStoreIndex)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import (SemanticSplitterNodeParser,
                                          SentenceSplitter)
# from llama_index.embeddings.anyscale import AnyscaleEmbedding
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

load_dotenv()


class Process(typing.NamedTuple):
    source: dict

    def _from_url(url: str) -> str:
        ic("downloading pdf")
        ic(url)
        response = requests.get(url)
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)
        text = ""
        ic("parsing pdf")
        for page_num in tqdm.tqdm(pdf_reader.pages):
            text += page_num.extract_text()
        return text

    def _from_local(filename) -> str:
        pdf_reader = PdfReader(filename)
        text = ""
        ic("parsing pdf")
        for page_num in tqdm.tqdm(pdf_reader.pages):
            text += page_num.extract_text()
        return text

    def parse_source(self):
        parsed_result = {k: v for k, v in self.source.items()}
        title = parsed_result["title"]
        doc_format = parsed_result.pop("doc_format")
        url = parsed_result.pop("url")
        local = parsed_result.pop("local")
        ic("parsing source:")
        ic(title)
        ic(doc_format)
        if doc_format == "pdf" and local != True:
            assert doc_format == url.split(".")[-1]
            parsed_result["text"] = _from_url(url)
            return parsed_result
        elif doc_format == "pdf" and local == True:
            parsed_result["text"] = _from_local(parsed_result.get("file"))
            return parsed_result
        else:
            logger.warn(f"Unknown document format {doc_format}")
            return None


class Documents:
    def __init__(self, data, published_list):
        self.data = data
        self.published_list = published_list

    @classmethod
    def from_file(cls, data, published_list):
        data = data
        published_list = published_list
        return cls(data, published_list)

    def _format_dict(self) -> list | None:
        """
        Format the given data into a list of Document objects.

        Args:
            published_list (list): A list of titles of already published documents.
            data (list): A list of dictionaries containing document information.

        Returns:
            list | None: A list of Document objects if there are new documents to be published,
                        or None if all documents in the data are already published.
        """
        print(self.data[0].keys())
        data = [x for x in self.data if x["title"] not in self.published_list]
        if len(data) > 0:
            documents = []
            for doc in data:
                document = Document(
                    text=doc["text"],
                    metadata={
                        "title": doc["title"],
                        "authors": doc["author(s)"],
                        "publish_date": doc["Publish Date"],
                        "description": doc["description"],
                        "document_type": doc["doc_type"],
                    },
                )
                ic(document.metadata["title"])
                documents.append(document)
            ic("Loaded Documents")
            return documents
        else:
            ic("No new documents to process")
            return None

    def gen_embeddings(self, vector_db="qdrant"):
        """Generate embeddings for the given published list and data.

        Args:
            published_list (list): A list of published items to be embedded.
            data (list): A list of data corresponding to the published items.

        Returns:
            None
        """
        if self.data != None:
            documents = self._format_dict()

            if isinstance(documents, list):

                ic("Creating Embeddings")

                embed_model = CohereEmbedding(
                    cohere_api_key=os.getenv("COHERE_API_PROD"),
                    model_name="embed-english-v3.0",
                    input_type="search_document",
                )
                Settings.embed_model = embed_model
                if vector_db == "qdrant":
                    qdrant_client = QdrantClient(
                        url=os.getenv("QDRANT_URL"),
                        api_key=os.getenv("QDRANT_API"),
                    )

                    vector_store = QdrantVectorStore(client=qdrant_client, collection_name="RAG_chunks")
                elif vector_db == "milvus":
                    vector_store = MilvusVectorStore(
                        dim=1024,
                        overwrite=False,
                        uri=os.getenv("MILVUS_URI"),
                        token=os.getenv("MILVUS_API"),
                        collection_name="RAG_chunks",
                    )
                else:
                    raise ValueError
                pipeline = IngestionPipeline(
                    transformations=[
                        SentenceSplitter(chunk_size=300, chunk_overlap=20),
                        # SemanticSplitterNodeParser.from_defaults(buffer_size =1, breakpoint_percentile_threshold = 95, embed_model=embed_model),
                        embed_model,
                    ],
                    vector_store=vector_store,
                    disable_cache=True,
                )

                nodes = pipeline.run(documents=documents, show_progress=True)

                ic(len(nodes))
                ic("Upload complete")

            else:
                pass
        else:
            ic("No new documents to process")
