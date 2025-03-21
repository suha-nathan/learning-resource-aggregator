import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from scripts.tagging_utils import generate_tags

load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

def fetch_and_store_google_books():
    client = MongoClient(MONGO_URI)
    db = client["learning_resources"]
    collection = db["resources"]

    query = "python programming"
    max_results = 40

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "maxResults": max_results,
        "key": GOOGLE_BOOKS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "items" not in data:
        print("No results from Google Books API.")
        return

    for item in data["items"]:
        volume = item["volumeInfo"]

        resource = {
            "title": volume.get("title"),
            "description": volume.get("description", ""),
            "source": "Google Books",
            "url": volume.get("infoLink"),
            "contentType": "book",
            "authors": volume.get("authors", []),
            "publisher": volume.get("publisher", ""),
            "categories": volume.get("categories", []),
            "isbn": next(
                (id["identifier"] for id in volume.get("industryIdentifiers", []) if id["type"] == "ISBN_13"),
                None
            )
        }
        
        tags = generate_tags(resource["title"], resource["description"])
        resource["tags"] = tags

        # Upsert (insert or update) into MongoDB to avoid duplicates
        collection.update_one(
            {"url": resource["url"]},
            {"$set": resource},
            upsert=True
        )

    print("Google Books data successfully fetched and stored.")

if __name__ == "__main__":
    fetch_and_store_google_books()
