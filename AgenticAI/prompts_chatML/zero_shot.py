from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

G_KEY = os.getenv('GEMINI_API_KEY')

client = OpenAI( 
    api_key=G_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

# Zero shot: The model is given direct question without any example 

SYSTEM_PROMPT = 'You are an expert in maths only answer maths related questions. Your name is Brody, and if the question is not related to maths just say sorry and dont answer'

res = client.chat.completions.create(
    model='gemini-2.5-flash',
    messages=[
        {'role':'system','content':SYSTEM_PROMPT},
        {'role': 'user', 'content': 'Hey There How are you! my name is Vipul'}
    ]
)

print(res.choices[0].message.content)