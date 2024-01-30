from pathlib import Path
import sys
import os
import qdrant_client
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    download_loader,
)
from llama_index.llms import Ollama
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore


def read_single_json(path):
    JSONReader = download_loader("JSONReader")
    loader = JSONReader()
    return loader.load_data(Path(path))


def read_single_pdf(path):
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    return loader.load_data(Path(path))


def create_qdrant_clinet(path):
    return qdrant_client.QdrantClient(path=path)


def create_collection(data_filename):
    basename = data_filename.split(".")[0].replace(" ", "_")
    extension = data_filename.split(".")[1]
    path = os.path.join("data", data_filename)
    match extension:
        case "pdf":
            loaded_documents = read_single_pdf(path)
        case "json":
            loaded_documents = read_single_json(path)
    return loaded_documents, basename


# definition of variables
data_filename = "Kocsis_Balazs_Phd_thesis.pdf"
llm = Ollama(model="mixtral")
client = create_qdrant_clinet(path="./qdrant_data")
documents, collection_name = create_collection(data_filename)


# define the vector database and index
vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
service_context = ServiceContext.from_defaults(llm=llm, embed_model="local")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents,
                                        service_context=service_context,
                                        storage_context=storage_context)
query_engine = index.as_query_engine(streaming=True)

# main CLI interaction loop
while True:
    query_message = input("Q: ")
    response = query_engine.query(query_message)
    response.print_response_stream()
    sys.stdout.flush()
    sys.stdout.write("\n")
