import schedule
import time
import os
from dotenv import load_dotenv
from scripts.fetch_google_books import fetch_and_store_google_books
from scripts.fetch_coursera import fetch_and_store_coursera_courses

load_dotenv()

def run_aggregation_job():
    print("Aggregation Job Started...")

    google_books_topics = ["Python programming", "Machine Learning", "Business", "Mathematics"]
    coursera_queries = ["machine learning", "python programming", "business analytics"]

    # Correct call to Google Books script
    for topic in google_books_topics:
        fetch_and_store_google_books(topic)

    # Corrected call to Coursera script
    for query in coursera_queries:
        fetch_and_store_coursera_courses(query)

    print("Aggregation Job Completed.")

schedule.every().day.at("00:00").do(run_aggregation_job)

if __name__ == "__main__":
    print("Scheduler script starting clearly...")
    run_aggregation_job()

    while True:
        schedule.run_pending()
        time.sleep(60)
