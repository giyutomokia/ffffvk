import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "movie_chatbot"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["dialogues"]

def scrape_script(movie_url, movie_name):
    response = requests.get(movie_url)
    soup = BeautifulSoup(response.text, "html.parser")

    dialogues = []
    current_character = None

    for line in soup.find_all("p"):
        text = line.get_text(strip=True)

        if text.isupper():  # Detect character names
            current_character = text
        elif current_character:
            dialogues.append({"movie": movie_name, "character": current_character, "dialogue": text})

    if dialogues:
        collection.insert_many(dialogues)
        print(f"Stored {len(dialogues)} dialogues for {movie_name}")

# Example usage
scrape_script("https://imsdb.com/scripts/Inception.html", "Inception")
