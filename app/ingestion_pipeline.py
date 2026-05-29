import os
from langchain_community.document_loaders import Docx2txtLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_documents(docs_path):
    loader = DirectoryLoader(
        path=docs_path,
        glob="*.docx",
        loader_cls=Docx2txtLoader
    )
    documents = loader.load()
    return documents


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_vector_store(chunks, dir):
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents = chunks,
        embedding = embedding_model,
        persist_directory = dir, 
        collection_metadata={"hnsw:space": "cosine"}
    )
    return vectorstore

def main():
    dir = "db/chroma_db"
    if os.path.exists(dir):
        print("Vector store already exists. No need to re-process documents.")
        
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = Chroma(
            persist_directory=dir,
            embedding_function=embedding_model, 
            collection_metadata={"hnsw:space": "cosine"}
        )
        print(f"Loaded existing vector store with {vectorstore._collection.count()} documents")
        return vectorstore
    
    print("Persistent directory does not exist. Initializing vector store...\n")
    
    documents = load_documents("docs")  
    chunks = split_documents(documents)
    vectorstore = create_vector_store(chunks, dir)
    
    print("\nIngestion complete!")
    return vectorstore

if __name__ == "__main__":
    main()
