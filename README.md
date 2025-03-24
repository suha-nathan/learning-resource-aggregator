# Learning Resource Aggregator

A data aggregation script that fetches publicly available learning resources (books, courses, etc.) from multiple sources like Google Books and Coursera. The meta-data collected and tagged from this service is meant to be used in a learning platform that enable users to build self-directed, topic-based learning plans using a range of resources. There is no collection of actual book/course data - only meta-data.

## Features

- Aggregates learning content from external APIs (e.g. Google Books, Coursera)
- Tags and categorizes content programmatically
- Stores resources in MongoDB with a flexible schema
- Runs scheduled fetch/update jobs via a containerized Python service
- Built with Docker Compose for local development and testing

## Project Structure

```
learning-resource-aggregator/
├── aggregation_service/
│   ├── scripts/                # Python scripts for fetching and tagging resources from various API
│   ├── scheduler.py            # Main job runner using `schedule` module
│   ├── Dockerfile              # Build config for the aggregator container
│   ├── .env                    # Environment variables for MongoDB URI
│   └── requirements.txt
├── mongo-data/                 # Docker volume for persistent MongoDB storage
├── docker-compose.yml
└── README.md
└── .env                        # Env variable for API key - accessible by yaml file
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/learning-resource-aggregator.git
cd learning-resource-aggregator
```

### 2. Set Up Environment Variables

Create a `.env` file in each of the following locations:

#### For Docker Compose (project root):

**`.env`**

```env
GOOGLE_BOOKS_API_KEY=<api key>
```

#### For Python aggregator service:

**`aggregation_service/.env`**

```env
MONGO_URI=mongodb://mongodb:27017
```

### 3. Create Folder at Project Root

Create the mongodb folder for persistent data storage between container rebuilds/removals. Specified by `docker-compose.yml`.

```bash
mkdir mongo-data
```

### 4. Build and Start the Project

```bash
docker compose up --build
```

This will:

- Start the MongoDB container and expose it at `localhost:27017`
- Start the aggregator container and run the scheduled resource fetch jobs

### 5. Manually Run the Aggregation Scripts (optional)

If you'd like to manually trigger the data collection (for testing):

```bash
docker exec -it resource_aggregator python scheduler.py
```

### 6. View Data in MongoDB

Use `mongosh`:

```bash
mongosh mongodb://localhost:27017
```

Then, within the mongosh:

```
use learning_resources
show collections
db.resources.find().pretty()
```

Or use [MongoDB Compass](https://www.mongodb.com/products/compass):

- Connection string: `mongodb://localhost:27017`

If data is unavailable outside the container - check that the port is correctly running the docker process.

```bash
lsof -i :27017
```

## Notes

- The aggregator fetches topics like `"Python programming"`, `"Machine Learning"`, etc.
- Tagging is handled programmatically using keyword-based rules.
- Coursera API access is unofficial — structure may change.
- Waiting on edX API Key approval

## To Do

- Topics to pull data from should be automated/not hard coded 
- Add support for additional APIs or RSS feeds
- Explore web scraping for unavailable learning resource meta-data
- Build frontend interface for searching resources
- Add error tracking and logging
