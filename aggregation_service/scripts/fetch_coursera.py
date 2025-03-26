import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from scripts.tagging_utils import generate_tags
from scripts.logger_utils import setup_logger

load_dotenv()
logger = setup_logger("coursera","fetch_coursera.log")

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
        logger.error(f"Failed to fetch Coursera data for query: {query}")
        return

    data = response.json()

    if "elements" not in data:
        logger.error(f"No results from Coursera API for query: {query}")
        return

    for course in data["elements"]:
        try:
            title = course.get("name")
            description = course.get("description", "")
            slug = course.get("slug", "")
            now = datetime.now(timezone.utc).isoformat()
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
                {
                    "$set": {
                        **resource,
                        "updatedAt": now
                    },
                    "$setOnInsert":{
                        "createdAt": now
                    }
                 },
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error fetching Coursera resource: {e}")

    logger.info(f"Coursera data successfully fetched and stored for query: {query}")

if __name__ == "__main__":
    queries = ["machine learning", "python programming", "business analytics"]
    for query in queries:
        fetch_and_store_coursera_courses(query)
