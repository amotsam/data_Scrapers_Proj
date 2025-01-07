import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from config import SCRAPER_CONFIGS
import utils
import json
from config import SCRAPER_CONFIGS



def config_forums_vars():
    with open("config.json") as f:
        config = json.load(f)
    scraper_name = "forums"  # Choose the scraper dynamically
    scraper_config = config[scraper_name]
    return scraper_config

def fetch_html(url, session, timeout=10):
    """Fetch the HTML content of a URL."""
    try:
        response = session.get(url, headers=SCRAPER_CONFIGS["forums"]["HEADERS"], timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None


def parse_data(html):
    """Parse the HTML content and extract required forum data."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        data = []

        # Extract all forum nodes
        forums = soup.find_all('div', class_='node')

        for forum in forums:
            # Extract the forum title and link
            title_element = forum.find('h3', class_='node-title')
            if not title_element:
                continue  # Skip if title is missing
            title = title_element.find('a').text.strip()
            link = title_element.find('a')['href']

            # Extract topics and messages
            topics_element = forum.find('dt', text='נושאים')
            messages_element = forum.find('dt', text='הודעות')

            # Get text for topics and messages
            topics_count = (
                topics_element.find_next('dd').text.strip() if topics_element else "0"
            )
            messages_count = (
                messages_element.find_next('dd').text.strip() if messages_element else "0"
            )

            # Append data
            data.append({
                "Title": title,
                "Link": link ,
                "Topics": topics_count,
                "Messages": messages_count
            })

        return data
    except Exception as e:
        logging.error(f"Failed to parse data: {e}")
        return []






