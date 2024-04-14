"""
    The Purpose of this file is to provide a wrapper around the PINECONE from langchain
"""

from langchain.schema.document import Document
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from pinecone import Pinecone
from neogpt.vectorstore.base import VectorStore

from neogpt.settings.config import (
    DEVICE_TYPE,
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    INDEX_NAME,
    MODEL_DIRECTORY,
    PINECONE_PERSIST_DIRECTORY,
)


class PineconeVectorStore(VectorStore):
    def __init__(self, api_key: str, environment: str) -> None:
        super().__init__()
        self.api_key = api_key
        self.environment = environment
        self.embeddings = HuggingFaceInstructEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": DEVICE_TYPE},
            cache_folder=MODEL_DIRECTORY,
        )
        self.pinecone_client = Pinecone(
            api_key=api_key,
            environment=environment,
            persist_directory=PINECONE_PERSIST_DIRECTORY,
            embedding_dimension=EMBEDDING_DIMENSION,
            index_name=INDEX_NAME,
            embedding_function=self.embeddings,
        )

    def from_documents(self, documents: list[Document]) -> Document:
        pinecone_data = []
        for document in documents:
            pinecone_data.append({"fields_name": document.fields_name})

        self.pinecone_client.upsert(pinecone_data)

    def as_retriever(self):
        return self.pinecone_client.as_retriever()


# api_key = "Your api key"
# environment = "your environment name"
# pinecone_store = PineconeVectoreStore(api_key, environment)
# pinecone_store.from_documents(documents)
