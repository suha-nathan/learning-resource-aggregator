import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from scripts.fetch_google_books import fetch_and_store_google_books
from scripts.fetch_coursera import fetch_and_store_coursera_courses
from scripts.logger_utils import setup_logger

load_dotenv()

# Setup logging
logger = setup_logger("scheduler", "aggregator.log")


def run_aggregation_job():
    logger.info("Aggregation Job Started")

    google_books_topics = ["Python programming", "Machine Learning", "Business", "Mathematics"]
    coursera_queries = ["machine learning", "python programming", "business analytics"]

    for topic in google_books_topics:
        try:
            logger.info(f"Fetching Google Books for: {topic}")
            fetch_and_store_google_books(topic)
            logger.info(f"Completed Google Books for: {topic}")
        except Exception as e:
            logger.error(f"Google Books fetch failed for '{topic}': {e}", exc_info=True)

    for query in coursera_queries:
        try:
            logger.info(f"Fetching Coursera courses for: {query}")
            fetch_and_store_coursera_courses(query)
            logger.info(f"Completed Coursera courses for: {query}")
        except Exception as e:
            logger.error(f"Coursera fetch failed for '{query}': {e}", exc_info=True)
    logger.info("Aggregation Job Completed")

schedule.every().day.at("00:00").do(run_aggregation_job)

if __name__ == "__main__":
    logger.info("Scheduler script starting...")
    run_aggregation_job()

    while True:
        schedule.run_pending()
        time.sleep(60)
