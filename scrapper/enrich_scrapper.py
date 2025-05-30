import os
import re
import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from cast_extraction import get_cast
import sys
load_dotenv()
headers = {'User-Agent': UserAgent().random}

def extract_movie_id(url):
    match = re.search(r'/title/(tt\d+)/', url)
    return match.group(1) if match else None

def extract_movie_details(url, release_year_from_csv):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        summary_tag = soup.find('span', {'data-testid': 'plot-l'}) or soup.find('span', {'data-testid': 'plot-xl'})
        summary = summary_tag.get_text(strip=True) if summary_tag else "N/A"

        directors = []
        credit_sections = soup.find_all('li', {'data-testid': 'title-pc-principal-credit'})
        for section in credit_sections:
            header = section.find('span', class_='ipc-metadata-list-item__label')
            if header and 'Director' in header.text:
                director_links = section.find_all('a')
                directors = [a.get_text(strip=True) for a in director_links]
                break

        rating_tag = soup.select_one('div[data-testid="hero-rating-bar__aggregate-rating__score"] > span')
        rating = rating_tag.get_text(strip=True).split('/')[0] if rating_tag else "N/A"

        title_header = soup.find('h1')
        movie_name = title_header.get_text(strip=True) if title_header else "N/A"

        return {
            'movie_name': movie_name,
            'release_year': release_year_from_csv,
            'director': ', '.join(directors) if directors else "N/A",
            'summary': summary,
            'rating': rating
        }

    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return {
            'movie_name': "N/A",
            'release_year': release_year_from_csv,
            'director': "N/A",
            'summary': "N/A",
            'rating': "N/A"
        }

def save_json(data, filepath, id_key=None, replace_on_key=None):
    existing_data = []

    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                pass

    if replace_on_key:
        replace_keys = {item[replace_on_key] for item in data if replace_on_key in item}
        existing_data = [item for item in existing_data if item.get(replace_on_key) not in replace_keys]

    combined_data = existing_data + data

    if id_key:
        deduped = {}
        for item in combined_data:
            deduped[item.get(id_key)] = item
        combined_data = list(deduped.values())

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=4, ensure_ascii=False)

def process_movie(row, cast_id_start):
    url = row['url']
    movie_id = extract_movie_id(url)
    print("printing movie id here: ", movie_id)
    if not movie_id:
        print("Skipping invalid URL:", url)
        return None, []

    movie_details = extract_movie_details(url, row['year'])  # Use year from CSV
    movie_record = {
        'id': movie_id,
        **movie_details
    }

    cast_list = get_cast(movie_id)
    casts = []
    for idx, (actor, character) in enumerate(cast_list):
        casts.append({
            'id': cast_id_start + idx,
            'movie_id': movie_id,
            'actor_name': actor,
            'character_name': character
        })

    return movie_record, casts

def main():
    genres = os.getenv("KEYWORDS", "")
    genre_list = [g.strip() for g in genres.split(',') if g.strip()]
    print(genre_list)
    
    all_dfs = []

    for genre in genre_list:
        file_path = f"masterdata/{genre}_results.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            all_dfs.append(df)
        else:
            print(f"File not found: {file_path}")

    if not all_dfs:
        print("No valid genre CSV files found. Exiting.")
        return

    full_df = pd.concat(all_dfs, ignore_index=True)

    full_df['unique_key'] = full_df['url'].apply(lambda x: extract_movie_id(x))
    full_df.drop_duplicates(subset='unique_key', inplace=True)

    movies_data = []
    casts_data = []
    cast_id_counter = 1

    full_df = full_df[:7]
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_movie, row, cast_id_counter + idx * 100): idx for idx, row in full_df.iterrows()}

        for future in as_completed(futures):
            movie_record, cast_entries = future.result()
            if movie_record:
                movies_data.append(movie_record)
                casts_data.extend(cast_entries)

    os.makedirs("../database", exist_ok=True)
    save_json(movies_data, "../database/movies.json", id_key='id')  # dedupe by movie id
    save_json(casts_data, "../database/casts.json", id_key='id', replace_on_key='movie_id')
    print("Data saved to `database/` folder.")

if __name__ == "__main__":
    main()
