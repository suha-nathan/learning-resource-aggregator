import schedule
import time
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from scripts.fetch_google_books import fetch_and_store_google_books
from scripts.fetch_coursera import fetch_and_store_coursera_courses

load_dotenv()

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "aggregator.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()  # Also show in console
    ]
)

def run_aggregation_job():
    logging.info("Aggregation Job Started")

    google_books_topics = ["Python programming", "Machine Learning", "Business", "Mathematics"]
    coursera_queries = ["machine learning", "python programming", "business analytics"]

    for topic in google_books_topics:
        try:
            logging.info(f"Fetching Google Books for: {topic}")
            fetch_and_store_google_books(topic)
            logging.info(f"Completed Google Books for: {topic}")
        except Exception as e:
            logging.error(f"Google Books fetch failed for '{topic}': {e}", exc_info=True)

    for query in coursera_queries:
        try:
            logging.info(f"Fetching Coursera courses for: {query}")
            fetch_and_store_coursera_courses(query)
            logging.info(f"Completed Coursera courses for: {query}")
        except Exception as e:
            logging.error(f"Coursera fetch failed for '{query}': {e}", exc_info=True)
    logging.info("Aggregation Job Completed")

schedule.every().day.at("00:00").do(run_aggregation_job)

if __name__ == "__main__":
    logging.info("Scheduler script starting...")
    run_aggregation_job()

    while True:
        schedule.run_pending()
        time.sleep(60)
