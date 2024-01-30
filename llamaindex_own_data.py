import sys
import os
import qdrant_client
from pathlib import Path
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    download_loader)
from llama_index.llms import Ollama
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore


def read_single_json(path: str):
    JSONReader = download_loader("JSONReader")
    loader = JSONReader()
    return loader.load_data(Path(path))


def read_single_pdf(path: str):
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    return loader.load_data(Path(path))


def create_qdrant_clinet(path: str):
    return qdrant_client.QdrantClient(path=path)


def create_collection(data_filename: str):
    basename = data_filename.split(".")[0].replace(" ", "_")
    extension = data_filename.split(".")[1]
    path = os.path.join("data", data_filename)
    match extension:
        case "pdf":
            loaded_documents = read_single_pdf(path)
        case "json":
            loaded_documents = read_single_json(path)
    return loaded_documents, basename


def initialize_qdrant(documents, client, collection_name, llm_model):
    """define the vector database and index
    :return
        query_engine index object
    """
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
    service_context = ServiceContext.from_defaults(llm=llm_model, embed_model="local")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents,
                                            service_context=service_context,
                                            storage_context=storage_context)
    query_engine = index.as_query_engine(streaming=True)
    return query_engine


if __name__ == "__main__":
    # definition of variables
    data_filename = "Kocsis_Balazs_Phd_thesis.pdf"
    llm_model = Ollama(model="mixtral")
    client = create_qdrant_clinet(path="./qdrant_data")
    documents, collection_name = create_collection(data_filename)
    query_engine = initialize_qdrant(documents, client, collection_name, llm_model)

    # main CLI interaction loop
    while True:
        query_message = input("Q: ")
        response = query_engine.query(query_message)
        response.print_response_stream()
        sys.stdout.flush()
        sys.stdout.write("\n")
