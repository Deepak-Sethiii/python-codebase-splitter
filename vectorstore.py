import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_vector_db():
    file_path = os.path.join("requests", "app.py")
    db_folder = "my_vector_db"

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        code_text = f.read()

    print(f"Loaded file ({len(code_text)} chars)")

    my_separators = ["\nclass ", "\ndef ", "\n\n", "\n", " ", ""]
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=my_separators,
        keep_separator=True
    )
    
    chunks = splitter.create_documents([code_text])
    print(f"Split into {len(chunks)} chunks.")

    print("Loading Embedding Model...")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Creating Vector Database...")
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_model, 
        persist_directory=db_folder
    )
    
    print(f"Success. Database saved to folder: {db_folder}")

if __name__ == "__main__":
    create_vector_db()
    