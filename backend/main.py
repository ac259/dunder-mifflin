from fastapi import FastAPI
from pydantic import BaseModel
from agents.schrute_bot.schrute_bot import get_response  # Update path if needed

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = get_response(request.message)  # Calls SchruteBot
    return {"response": response}

@app.get("/")
async def home():
    return {"message": "Dunder Mifflin AI Backend Running"}
