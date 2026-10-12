import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)
output = client.interactions.create(model="gemini-3.8-flash", input="こんにちは、元気ですか？")
print(output.output_text)