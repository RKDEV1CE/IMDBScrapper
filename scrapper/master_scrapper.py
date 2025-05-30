import os
import json
import time
import multiprocessing
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

KEYWORDS = os.getenv("KEYWORDS", "")
KEYWORDS = [kw.strip() for kw in KEYWORDS.split(",") if kw.strip()]

ITERATION_MAPPING = os.getenv("ITERATION_MAPPING", "{}")
ITERATION_MAPPING = json.loads(ITERATION_MAPPING)

BASE_URL = "https://www.imdb.com"
OUTPUT_DIR = Path("masterdata")
OUTPUT_DIR.mkdir(exist_ok=True)

BUTTON_XPATH = '//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/div/span/button/span/span'
LI_XPATH = '//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li'

def scrape_keyword(keyword: str, iteration_count: int):
    print(f"Starting scrape for '{keyword}' with {iteration_count} iterations")
    
    # Setup browser
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        search_url = f"{BASE_URL}/find/?q={keyword}&s=tt&ttype=ft&ref_=fn_ft"
        driver.get(search_url)
        time.sleep(2)

        for i in range(iteration_count):
            try:
                print(f"[{keyword}] Clicking button {i+1}/{iteration_count}")
                button = wait.until(EC.element_to_be_clickable((By.XPATH, BUTTON_XPATH)))
                try:
                    button.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
            except TimeoutException:
                print(f"[{keyword}] Button not found or exhausted.")
                break

        results = []

        lis = driver.find_elements(By.XPATH, LI_XPATH)
        print(f"[{keyword}]  Found {len(lis)} results")

        for idx, li in enumerate(lis):
            try:
                title_anchor = li.find_element(By.TAG_NAME, "a")
                title = title_anchor.text.strip()
                href = title_anchor.get_attribute("href")
                text_lines = li.text.split('\n')
                year = text_lines[1].strip() if len(text_lines) > 1 else "N/A"
                cast = text_lines[2].strip() if len(text_lines) > 2 else "N/A"

                results.append({
                    "title": title,
                    "year": year,
                    "cast": cast,
                    "url": href
                })

            except Exception as e:
                print(f"[{keyword}] Error in item {idx+1}: {e}")
                continue

        output_file = OUTPUT_DIR / f"{keyword}_results.csv"

        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False, encoding="utf-8")

        print(f"[{keyword}] Done ({len(results)} results)")

    finally:
        driver.quit()

def main():
    processes = []

    for keyword in KEYWORDS:
        iteration = ITERATION_MAPPING.get(keyword, 2)  # Default to 2 if not found
        p = multiprocessing.Process(target=scrape_keyword, args=(keyword, iteration))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
