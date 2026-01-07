import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print(" Error: API Key not found in .env")
    exit()

print("contacting Google")

try:
    genai.configure(api_key=api_key)
    for m in genai.list_models():
        print(f"Found: {m.name}")

except Exception as e:
    print(f" Error: {e}")