from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

G_KEY = os.getenv('GEMINI_API_KEY')

# Chain of thaught prompting 

SYSTEM_PROMPT = """You are a helpful AI assistant named Brody.

For every request respond ONLY in this JSON format, no extra text:
{
    "step": "think" | "plan" | "output",
    "content": "your content here"
}

Follow steps in order:

STEP 1 - think: Understand what the user is asking and break it down.
STEP 2 - plan: Decide the best approach to solve it.
STEP 3 - output: Give the final answer to the user.

Never skip steps. Never respond outside JSON format.

Rules:
- The "content" field must ALWAYS be a plain string. Never return nested JSON or objects inside content.
- Never answer questions outside your defined steps.
- Always complete all 3 steps before giving output.
- Keep think and plan steps concise, save detail for output.
- If you don't know something, say so in the output step.
- Never make up facts.
"""

client = OpenAI(
    api_key=G_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



def run_agent(user_input):

    message_history = [
        {'role':'system','content':SYSTEM_PROMPT},
        {'role':'user','content':user_input}]

    while True:
        res = client.chat.completions.create(
            model='gemini-2.5-flash-lite',
            response_format={'type':'json_object'},
            messages=message_history
        )

        raw_res = res.choices[0].message.content
        message_history.append({"role":'assistant','content':raw_res})
        parsed_res = json.loads(raw_res)

        if(parsed_res.get('step') == 'think'):
            print('🔥 ', parsed_res.get('content') )
            continue

        if(parsed_res.get('step') == 'plan'):
            print('🧠', parsed_res.get('content'))
            continue

        if(parsed_res.get('step') == 'output'):
            print('😁', parsed_res.get('content'))
            break


if __name__ == '__main__':

    while True:
        print('\n')

        user_query = input('👉 ')

        if user_query.strip().lower() == 'q' or user_query.strip() == '':
            break

        run_agent(user_query)
    
        print('\n')




