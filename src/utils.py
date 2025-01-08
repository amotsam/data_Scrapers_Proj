import pandas as pd
import logging
import requests
from urllib3 import Retry
from requests.adapters import HTTPAdapter
import os
from config import SCRAPER_CONFIGS

def save_to_csv(data, file_path):
    """Save the extracted data to a CSV file."""
    try:
        ensure_directory_exists(file_path)  # Ensure the directory exists
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, encoding='utf-8')
        logging.info(f"Data saved successfully to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save data to {file_path}: {e}")


def Init_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_html(url,session,domain):
    """Fetch the HTML content of a URL."""

    try:
        response = session.get(url, headers=SCRAPER_CONFIGS[f"{domain}"]["HEADERS"])
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def ensure_directory_exists(file_path):
    """
    Ensure that the directory for the given file path exists.
    If it doesn't exist, create it.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
