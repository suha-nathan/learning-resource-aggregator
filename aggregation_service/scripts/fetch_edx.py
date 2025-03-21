import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")

def fetch_and_store_edx_courses():
    client = MongoClient(MONGO_URI)
    db = client["learning_resources"]
    collection = db["resources"]

    EDX_COURSES_API = "https://api.edx.org/catalog/v1/catalogs/"
# https://course-catalog-api-guide.readthedocs.io/en/latest/index.html
    params = {
        "subject": "Computer Science",
        "language": "English",
        "availability": "Available now",
        "page_size": 50
    }

    response = requests.get(EDX_COURSES_API, params=params)
    if response.status_code != 200:
        print("Failed to fetch data from EdX API.")
        return

    data = response.json()

    if "objects" not in data:
        print("No results from EdX API.")
        return

    for course in data["objects"]["results"]:
        resource = {
            "title": course.get("title"),
            "description": course.get("full_description", ""),
            "tags": ["Computer Science", "Course"],
            "source": "EdX",
            "url": course.get("marketing_url"),
            "contentType": "course",
            "difficulty": course.get("level_type", ""),
            "provider": course.get("owners", [{}])[0].get("name", ""),
            "duration": course.get("weeks_to_complete", ""),
            "instructors": [instructor.get("name") for instructor in course.get("instructors", [])]
        }

        collection.update_one(
            {"url": resource["url"]},
            {"$set": resource},
            upsert=True
        )

    print("EdX course data successfully fetched and stored.")

if __name__ == "__main__":
    fetch_and_store_edx_courses()
