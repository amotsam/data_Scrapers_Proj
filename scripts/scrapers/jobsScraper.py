import requests
from bs4 import BeautifulSoup
import logging
from config import SCRAPER_CONFIGS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_html(url, session, timeout=10):
    """Fetch the HTML content of a URL."""
    try:
        response = session.get(url, headers=SCRAPER_CONFIGS["jobs"]["HEADERS"], timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None


def parse_data(html):
    """Parse the HTML content and extract required job data."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        data = []

        # Extract all job nodes
        job_listings = soup.find_all('div', class_='job-item-main')

        for job in job_listings:
            # Extract job details
            title = job.find('h3', class_='display-28').text.strip() if job.find('h3', class_='display-28') else 'N/A'
            company = job.find('p', class_='display-22').text.strip() if job.find('p', class_='display-22') else 'N/A'
            location = job.find('span', class_='display-18').text.strip() if job.find('span', class_='display-18') else 'N/A'
            description = job.find('p', class_='display-18').text.strip() if job.find('p', class_='display-18') else 'N/A'

            # Append data
            data.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Description": description
            })

        return data
    except Exception as e:
        logging.error(f"Failed to parse data: {e}")
        return []
