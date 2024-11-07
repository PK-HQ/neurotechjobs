import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# Function to fetch job listings from Indeed based on a query and location
def fetch_jobs(query, location, num_pages=1):
    job_list = []
    for page in range(num_pages):
        url = f"https://www.indeed.com/jobs?q={query}&l={location}&start={page * 10}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for job_card in soup.find_all('div', class_='jobsearch-SerpJobCard'):
            title = job_card.find('h2', class_='title').text.strip()
            company = job_card.find('span', class_='company').text.strip()
            location = job_card.find('div', class_='location').text.strip() if job_card.find('div',
                                                                                             class_='location') else None
            summary = job_card.find('div', class_='summary').text.strip()
            link = 'https://www.indeed.com' + job_card.find('a')['href']

            job_list.append({
                'Title': title,
                'Company': company,
                'Location': location,
                'Summary': summary,
                'Link': link
            })

        time.sleep(1)  # Be considerate to Indeed's servers

    return pd.DataFrame(job_list)


# Example Usage
if __name__ == "__main__":
    # Set your search criteria here
    job_query = "neural data scientist"
    job_location = "Austin, TX"

    # Fetch jobs and save to Excel
    job_data = fetch_jobs(job_query, job_location, num_pages=2)  # Set num_pages as desired
    job_data.to_excel("Indeed_Jobs.xlsx", index=False)
    print("Job data saved to Indeed_Jobs.xlsx")
