# 🎬 IMDb Movie Scraper & API Service

A modular Python-based project to scrape IMDb movie data by genre keywords (like Action, Drama, Comedy), enrich it with detailed metadata, and serve it through RESTful APIs.

---

## 📊 Architecture Diagram
![image](https://github.com/user-attachments/assets/38087e50-5480-4387-b056-5120ae1ebdd8)

## Problem Objective

We aim to scrape movie information from IMDb based on genre keywords such as Action, Drama, or Comedy. This project collects, enriches, and serves movie data via REST APIs.

---

## How IMDb Works (Observations)

- Searching a genre keyword on IMDb shows a list of movies after applying a filter.
- Clicking "More popular movies" dynamically loads more content.
- Each movie link contains a unique IMDb movie ID, for example:  
  https://www.imdb.com/title/tt0078732/
- Cast details are available at a fixed pattern URL:  
  https://www.imdb.com/title/<movie_id>/fullcredits/

---

## Tech Stack

- Python  
- Selenium  
- BeautifulSoup  
- Docker  
- Django Rest Framework

---

## Modules

### 1. Master Data Scraper

- Scrapes the initial list of movies based on a keyword (e.g., Action).
- Stores the movie ID and release year.
- Since the list is mostly static (until new releases), this is a one-time process.
- A lightweight weekly cron job can check for new additions.

### 2. Enrichment Scraper

- Takes movie_id from Master Data and scrapes:
  - Rating
  - Director
  - Description
  - Cast list
- All information is stored in the database (movie.json & casts.json) and linked to the original movie entry.

### 3. Backend Development

- REST APIs are built to serve the data using Django Rest Framework.
- Current endpoints include:
  - GET /api/movies/?release_year=YYYY — Filter by year
  - GET /api/casts/?movie_id=ttXXXX — Get cast by movie ID

---

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/RKDEV1CE/IMDBScrapper.git  
cd IMDBScrapper

### 2. Set Up Virtual Environment

python -m venv venv

Activate the virtual environment:

- On Windows (CMD):  
  venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

---

## Module Breakdown

### Master Module

This module scrapes movie data (movie ID and release year) based on keywords and stores the output as master data.

**Steps:**

- Edit the `.env` file in the root directory with your desired keywords for scraping.

Run the scraper:
cd scrapper
python master_scrapper.py

Scraped data will be saved in the `scrapper/masterdata/` directory, categorized by keyword and save files in format <keyword>_results.csv.

### Enrich Module

This module processes the master data and transforms it into enriched JSON files saved in the `database/` folder and save file <casts.json> & <movies.json>.

To run:
cd scrapper
python enrich_scrapper.py

### Backend Module

This module serves the enriched data through API endpoints.

**Steps:**

- Import the Postman collection from the `postmancollection/` folder into Postman.
- Start the backend using Docker:

docker-compose up --build

- Inside the Docker container, run:

python manage.py migrate  
python manage.py load_data

**Verify the data is loaded:**

python manage.py shell

Then, in the shell:

from movies.models import Movie, Cast  
Movie.objects.count()  
Cast.objects.count()

Now you can use Postman to hit the available API endpoints and interact with the data.

---

**Large Dataset path:**
i) movies&cast: database\largedataset
ii) master data: scrapper\masterdata\large_dataset
 
## Future Scope

### Serverless Execution
Migrate the master and enrich scrapers to a serverless architecture (e.g., GCP Cloud Run Jobs) to handle concurrent processing of multiple keyword files.
### Search Enhancements
Add advanced search functionality to the API using fuzzy matching and Elasticsearch for better keyword-based movie retrieval.