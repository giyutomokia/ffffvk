from database import collection
from fuzzywuzzy import process
from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def find_closest_dialogue(user_message, character=None):
    # Fetch all dialogues from DB
    query = {"character": character} if character else {}
    all_dialogues = [doc["dialogue"] for doc in collection.find(query)]

    # Find the closest match
    best_match = process.extractOne(user_message, all_dialogues, score_cutoff=75)
    return best_match[0] if best_match else None

def generate_ai_response(user_message):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message["content"]
