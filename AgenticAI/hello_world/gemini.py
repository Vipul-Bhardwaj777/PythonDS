from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

G_KEY = os.getenv('GEMINI_API_KEY')

client = genai.Client(
    api_key= G_KEY,
)

res = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Explain how ai works in few words'
)

print(res.text)