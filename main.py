# main.py

from modules.scraper import fetch_jobs
from modules.data_exporter import save_to_excel

if __name__ == "__main__":
    # Fetch job data with dynamic query from manually set keywords
    job_data = fetch_jobs()

    # Save data to Excel
    save_to_excel(job_data)
