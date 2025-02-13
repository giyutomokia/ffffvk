from fastapi import FastAPI
from models import ChatRequest
from chatbot import find_closest_dialogue, generate_ai_response

app = FastAPI()

@app.post("/chat")
async def chat(request: ChatRequest):
    match = find_closest_dialogue(request.user_message, request.character)
    
    if match:
        return {"response": match}
    else:
        ai_response = generate_ai_response(request.user_message)
        return {"response": ai_response}
