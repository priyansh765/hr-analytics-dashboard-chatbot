from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

PDF_PATH = "data/policies/hr_policy.pdf"
VECTOR_DB_PATH = "data/vectorstore"

def build_vector_store():
    print("PDF load ho raha hai...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"Total pages loaded: {len(documents)}")

    print("Text ko chunks me toda jaa raha hai...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")

    print("Embedding model load ho raha hai (pehli baar thoda time lega)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Vector database ban raha hai...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH,
    )
    print(f"Vector database ban gaya aur save ho gaya: {VECTOR_DB_PATH}")

    return vectorstore

if __name__ == "__main__":
    build_vector_store()
    print("\n✅ Done! Ab RAG chatbot ready hai use karne ke liye.")