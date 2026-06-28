from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()

client = Client(host="http://localhost:11434/")


@app.get("/")
def root_read():
    return {"message": "Hello World"}


@app.get("/contact-us")
def read_root():
    return {"email": "contactus@gmail.com"}


@app.post("/chat")
def chat(message: str = Body(..., description="The message")):
    res = client.chat(
        model="gemma2:2b", messages=[{"role": "user", "content": message}]
    )

    return {"response": res.message.content}
