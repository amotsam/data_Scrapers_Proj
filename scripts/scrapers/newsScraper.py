import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

def fetch_html(url, session, timeout=10):
    """Fetch the HTML content of a URL."""
    try:
        response = session.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def parse_data(html):
    """Parse the HTML content and extract required news data."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        data = []

        # Extract all articles
        articles = soup.find_all('div', class_='slotView')  # Adjust based on current structure

        for article in articles:
            # Extract the news title
            header_element = article.find('a', class_='slotTitle')
            header = header_element.text.strip() if header_element else "N/A"
            link = header_element['href'] if header_element and 'href' in header_element.attrs else "N/A"

            # Extract the news summary
            summary_element = article.find('div', class_='slotSubTitle')
            summary = summary_element.text.strip() if summary_element else "N/A"

            # Extract or generate datetime
            time_element = article.find('span', class_='timestamp')
            datetime_value = time_element.text.strip() if time_element else datetime.now().isoformat()

            # Append data
            data.append({
                "Header": header,
                "Link": link,
                "Summary": summary,
                "DateTime": datetime_value
            })

        return data
    except Exception as e:
        logging.error(f"Failed to parse data: {e}")
        return []
