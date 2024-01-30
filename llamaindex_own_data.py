from pathlib import Path
import sys
from PyPDF2 import PdfReader
import qdrant_client
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    download_loader,
)
from llama_index.llms import Ollama
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore


def read_json(path):
    JSONReader = download_loader("JSONReader")
    loader = JSONReader()
    return loader.load_data(Path(path))


def read_pdf(path):
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    return loader.load_data(Path(path))

# documents, collection_name = read_json('./data/tinytweets.json'), "tweets"
documents, collection_name = read_pdf("./data/Kocsis_Balazs_Phd_thesis.pdf"), "my_thesis"


client = qdrant_client.QdrantClient(
    path="./qdrant_data"
)
vector_store = QdrantVectorStore(client=client,
                                 collection_name=collection_name)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

llm = Ollama(model="mixtral")
service_context = ServiceContext.from_defaults(llm=llm,
                                               embed_model="local")

index = VectorStoreIndex.from_documents(documents,
                                        service_context=service_context,
                                        storage_context=storage_context)

query_engine = index.as_query_engine(streaming=True)
while True:
    query_message = input("Q: ")

    response = query_engine.query(query_message)

    response.print_response_stream()

    sys.stdout.flush()
    sys.stdout.write("\n")