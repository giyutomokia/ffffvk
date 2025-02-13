from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

# Replace with your OpenAI API key
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

# Define character personalities
CHARACTER_PERSONALITIES = {
    "yoda": "Wise and cryptic, speaks in reversed sentence structure.",
    "joker": "Chaotic and playful, with a dark sense of humor.",
    "ironman": "Witty, sarcastic, and confident, with a tech-savvy mind."
}

class ChatRequest(BaseModel):
    character: str
    user_message: str
@app.get("/")  # This handles GET requests to the root ("/") path
def home():
    return {"message": "Welcome to the Movie Character Chatbot API! Use /chat to talk to a character."}
@app.get("/chat")
def chat_info():
    return {"message": "Use POST /chat with {'character': 'joker', 'user_message': 'your message'}"}

@app.post("/chat")
def chat(request: ChatRequest):
    character = request.character.lower()
    user_message = request.user_message

    if character not in CHARACTER_PERSONALITIES:
        return {"error": "Character not found! Choose from: Yoda, Joker, Ironman."}
    
    personality = CHARACTER_PERSONALITIES[character]
    prompt = f"You are {character}, {personality} Respond to: {user_message}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_message}]
    )
    
    return {"character": character, "response": response["choices"][0]["message"]["content"]}
