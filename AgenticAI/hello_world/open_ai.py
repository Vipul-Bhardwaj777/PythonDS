from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

G_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(  # Remove all the params if open ai key is there in env
    api_key=G_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

res = client.chat.completions.create(
    model="gemini-2.5-flash",  # use gpt models if open ai key is there
    messages=[
        {
            "role": "system",
            "content": "You are an expert in maths only answer maths related questions. And if the question is not related to maths just say sorry and dont answer",
        },
        {"role": "user", "content": "Hey There How are you! my name is Vipul"},
    ],
)

print(res.choices[0].message.content)
