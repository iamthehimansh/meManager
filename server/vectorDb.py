from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

from langchain.vectorstores.chroma import Chroma
import os
import shutil
import time
CHROMA_PATH = "../data/chroma"
# DATA_PATH = "data-constitution"
DATA_PATH="../data/toTrain"

def main():
    t1=time.time()
    generate_data_store()
    print(time.time()-t1)


def generate_data_store():
    documents = load_documents()
    with open("data.txt", "w") as f:
        for doc in documents:
            f.write(doc.page_content)
            f.write("\n\n") 


def load_documents():
    loader = DirectoryLoader(DATA_PATH)
    documents = loader.load()
    return documents


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=450,
        chunk_overlap=150,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # document = chunks[10]
    # print(document.page_content)
    # print(document.metadata)

    return chunks


def save_to_chroma(chunks):
    # Clear out the database first.
    # if os.path.exists(CHROMA_PATH):
    #     shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    # db = Chroma.from_documents(
    #     chunks, OllamaEmbeddings(model="Aarohan"), persist_directory=CHROMA_PATH
    # )
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function= OllamaEmbeddings(model="mxbai-embed-large"))
    db.add_documents(chunks)
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    os.system("clear && pwd")
    print(os.curdir)
    main()