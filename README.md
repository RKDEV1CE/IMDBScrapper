IMDb Movie Scraper & API Service

Architecture diagram:
![image](https://github.com/user-attachments/assets/38087e50-5480-4387-b056-5120ae1ebdd8)

Problem Objective:
We aim to scrape movie information from IMDb based on genre keywords such as Action, Drama, or Comedy. This project collects, enriches, and serves movie data via REST APIs.

How IMDb Works (Observations):
Searching a genre keyword on IMDb shows a list of movies after applying a filter.
Clicking "More popular movies" dynamically loads more content.
Each movie link contains a unique IMDb movie ID, e.g.:
https://www.imdb.com/title/tt0078732/
Cast details are available at a fixed pattern URL:
https://www.imdb.com/title/<movie_id>/fullcredits/

Tech Stack:
Python
Selenium
BeautifulSoup
Docker
Django Rest Framework

Modules:
1)Master Data Scraper
🔹 Scrapes the initial list of movies based on a keyword (e.g., Action).
🔹 Stores the movie ID and release year.
🔹 Since the list is mostly static (until new releases), this is a one-time process.
🔹 A lightweight weekly cron job can check for new additions.

2)Enrichment Scraper
🔹 Takes movie_id from Master Data and scrapes:
Rating
Director
Description
Cast list
🔹 All information is stored in the database and linked to the original movie entry.

3️)Backend Development
🔹 REST APIs are built to serve the data using Django Rest Framework.
🔹 Current endpoints include:
GET /api/movies/ — List of movies
GET /api/movies/?release_year=YYYY — Filter by year
GET /api/casts/?movie_id=ttXXXX — Get cast by movie ID

