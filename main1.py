import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Gemini API key not found!")
    exit()

client = genai.Client(api_key=api_key)

response = client.interactions.create(
    model="gemini-3.7-flash",
    input="Say hello to me in one sentence. This is an API test."
)

print("\n✅ Gemini is working!")
print(response.output_text)