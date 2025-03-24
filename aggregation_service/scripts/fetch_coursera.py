import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from scripts.tagging_utils import generate_tags

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")

def fetch_and_store_coursera_courses(query):
    client = MongoClient(MONGO_URI)
    db = client["learning_resources"]
    collection = db["resources"]

    endpoint = "https://api.coursera.org/api/courses.v1" #unofficial API endpoint for coursera
    params = {
        "q": "search",
        "query": query,
        "includes": "partnerIds,instructorIds",
        "fields": "description,primaryLanguages,workload"
    }

    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch Coursera data for query: {query}")
        return

    data = response.json()

    if "elements" not in data:
        print(f"No results from Coursera API for query: {query}")
        return

    for course in data["elements"]:
        title = course.get("name")
        description = course.get("description", "")
        slug = course.get("slug", "")
        resource = {
            "title": title,
            "description": description,
            "tags": generate_tags(title, description),
            "source": "Coursera",
            "url": f"https://www.coursera.org/learn/{slug}",
            "contentType": "course",
            "provider": "Coursera",
            "difficulty": course.get("workload", ""),
            "duration": None,  # Coursera API doesn't directly provide duration
            "instructors": [],  # Additional API calls needed for detailed instructor info
        }

        collection.update_one(
            {"url": resource["url"]},
            {"$set": resource},
            upsert=True
        )

    print(f"Coursera data successfully fetched and stored for query: {query}")

if __name__ == "__main__":
    queries = ["machine learning", "python programming", "business analytics"]
    for query in queries:
        fetch_and_store_coursera_courses(query)
