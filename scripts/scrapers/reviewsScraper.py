import requests
from bs4 import BeautifulSoup
import logging

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
    """Parse the HTML content and extract review data."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        data = []

        # Find all review containers
        review_divs = soup.find_all('div', class_='BGComments')

        for div in review_divs:
            # Extract movie name
            movie_link = div.find('a', class_='DarkGreenStrong14')
            movie_name = movie_link.text.strip() if movie_link else "Unknown"

            # Extract review text
            review_text_element = div.find('span', class_='DarkGreenStrong14')
            review_text = review_text_element.text.strip() if review_text_element else "No Review"

            # Extract rating
            rating_element = div.find('span', class_='DarkGreenStrong30')
            rating = rating_element.text.strip() if rating_element else "No Rating"

            # Append the extracted data
            data.append({
                "Movie": movie_name,
                "Review": review_text,
                "Rating": rating
            })

        return data
    except Exception as e:
        logging.error(f"Error parsing data: {e}")
        return []
