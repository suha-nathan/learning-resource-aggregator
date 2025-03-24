import schedule
import time
import os
from dotenv import load_dotenv
# from scripts.fetch_edx import fetch_and_store_edx_courses
from scripts.fetch_google_books import fetch_and_store_google_books
from scripts.fetch_coursera import fetch_and_store_coursera_courses

# Load environment variables from .env
load_dotenv()

def run_aggregation_job():
    print("Aggregation Job Started...")
    
    try:
        fetch_and_store_coursera_courses()
        fetch_and_store_google_books()
    except Exception as e:
        print(f"Error during aggregation job: {e}")

    print("Aggregation Job Completed.")

# Schedule job every day at midnight (change as needed)
schedule.every().day.at("00:00").do(run_aggregation_job)

if __name__ == "__main__":
    print("Scheduler running. Waiting for next scheduled job...")

    # Run job immediately on startup
    run_aggregation_job()

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
