import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from scripts.tagging_utils import generate_tags

load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")

def fetch_and_store_google_books(topic):
    client = MongoClient(MONGO_URI)
    db = client["learning_resources"]
    collection = db["resources"]

    max_results = 40

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": topic,
        "maxResults": max_results,
        "key": GOOGLE_BOOKS_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch data from Google Books API for topic: {topic}")
        return

    data = response.json()

    if "items" not in data:
        print(f"No results found on Google Books API for topic: {topic}")
        return

    for item in data["items"]:
        volume = item["volumeInfo"]

        title = volume.get("title", "")
        description = volume.get("description", "")

        resource = {
            "title": title,
            "description": description,
            "tags": generate_tags(title, description),
            "source": "Google Books",
            "url": volume.get("infoLink", ""),
            "contentType": "book",
            "authors": volume.get("authors", []),
            "publisher": volume.get("publisher", ""),
            "categories": volume.get("categories", []),
            "isbn": next(
                (id["identifier"] for id in volume.get("industryIdentifiers", []) if id["type"] == "ISBN_13"),
                None
            )
        }
        print(f"Inserting resource into DB: {resource['title']}")
        collection.update_one(
            {"url": resource["url"]},
            {"$set": resource},
            upsert=True
        )
    print(f"MongoDB URI used: {MONGO_URI}")
    print(f"Google Books data successfully fetched and stored for topic: {topic}")

if __name__ == "__main__":
    topics = ["Python programming", "Machine Learning", "Business", "Mathematics"]
    for topic in topics:
        fetch_and_store_google_books(topic)
