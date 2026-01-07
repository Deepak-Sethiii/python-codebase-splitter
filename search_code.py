import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def search_codebase(query):
    db_folder = "my_vector_db"
    
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = Chroma(persist_directory=db_folder, embedding_function=embedding_model)

    results = db.similarity_search(query, k=3)

    print(f"Results for: {query}")
    print("=" * 50)
    
    for i, doc in enumerate(results):
        print(f"Result {i+1}:")
        print(doc.page_content)
        print("-" * 50)

if __name__ == "__main__":
    user_query = "What is the login function?"
    search_codebase(user_query)