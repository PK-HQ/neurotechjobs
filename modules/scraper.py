# modules/scraper.py

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from config.settings import DEFAULT_LOCATION, NUM_PAGES
from modules.query_builder import generate_dynamic_query


def fetch_jobs(num_pages=NUM_PAGES):
    """Fetch job listings from Indeed based on a dynamically generated query."""
    query = generate_dynamic_query()
    job_list = []

    for page in range(num_pages):
        url = f"https://www.indeed.com/jobs?q={query}&l={DEFAULT_LOCATION}&start={page * 10}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(url, headers=headers)

        # debug
        print(response.status_code)
        print(response.text[:1000])  # Print the first 1000 characters to see what’s being returned

        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for a new structure or alternative class names for job listings
        for job_card in soup.find_all('div', class_='job_seen_beacon'):  # Adjusted to a common class used by Indeed
            try:
                title = job_card.find('h2', class_='jobTitle').text.strip()
            except AttributeError:
                title = "No Title Found"
            try:
                company = job_card.find('span', class_='companyName').text.strip()
            except AttributeError:
                company = "No Company Found"
            try:
                location = job_card.find('div', class_='companyLocation').text.strip()
            except AttributeError:
                location = "No Location Found"
            try:
                summary = job_card.find('div', class_='job-snippet').text.strip()
            except AttributeError:
                summary = "No Summary Found"
            try:
                link = 'https://www.indeed.com' + job_card.find('a')['href']
            except TypeError:
                link = "No Link Found"

            job_list.append({
                'Title': title,
                'Company': company,
                'Location': location,
                'Summary': summary,
                'Link': link
            })

        time.sleep(1)  # Be considerate to Indeed's servers

    if not job_list:
        print("No job listings found. Please double-check the HTML structure or selectors.")

    return pd.DataFrame(job_list)
