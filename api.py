import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# --- UPDATED IMPORTS ---
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate # <--- CHANGED THIS LINE
# -----------------------

# 1. Load Keys
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("API Key missing. Please ensure GOOGLE_API_KEY is set in your .env file.")

# 2. Setup App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load Brain
db_folder = "my_vector_db"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory=db_folder, embedding_function=embedding_model)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-002",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# 4. Chat Endpoint
class UserRequest(BaseModel):
    question: str

@app.post("/chat")
def chat_endpoint(request: UserRequest):
    user_query = request.question
    print(f"Incoming Question: {user_query}")

    results = db.similarity_search(user_query, k=3)
    
    # Safety check if no code is found
    if not results:
        return {"answer": "I couldn't find any relevant code."}

    context_text = "\n\n".join([doc.page_content for doc in results])

    template = """
    You are an expert Python developer. Answer the question based ONLY on the following code snippets.
    
    CODE CONTEXT:
    {context}

    USER QUESTION: 
    {question}

    ANSWER:
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    response = chain.invoke({"context": context_text, "question": user_query})
    
    return {"answer": response.content}