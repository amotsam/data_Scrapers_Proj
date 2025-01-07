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
    """Parse the HTML content and extract shopping product data."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        data = []

        # Find all product containers
        products = soup.find_all('div', class_='product-inner')

        for product in products:
            # Extract product name
            name_element = product.find('h2', class_='woocommerce-loop-product__title')
            name = name_element.text.strip() if name_element else "No Name"

            # Extract product price (handles ranges)
            price_element = product.find('span', class_='woocommerce-Price-amount')
            if price_element:
                price = price_element.text.strip()
            else:
                price = "No Price"

            # Extract product rating
            rating_element = product.find('strong', class_='rating')
            rating = rating_element.text.strip() if rating_element else "No Rating"

            # Extract product categories
            categories_element = product.find('span', class_='loop-product-categories')
            categories = categories_element.text.strip() if categories_element else "No Categories"

            # Append product details to the list
            data.append({
                "Name": name,
                "Price": price,
                "Rating": rating,
                "Categories": categories
            })

        return data
    except Exception as e:
        logging.error(f"Error parsing data: {e}")
        return []
