from bs4 import BeautifulSoup
import logging
from datetime import datetime

def parse_data(html):
    """Parse the HTML content and extract required news data."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        data = []

        # Extract all articles with headers
        articles = soup.find_all('h2', class_='slotTitle medium')  # Adjust based on structure

        for article in articles:
            # Extract the news title from the <span>
            span_element = article.find('span')
            header = span_element.text.strip() if span_element else "N/A"

            # Extract link from the parent <a> if available
            link_element = article.find_parent('a')
            link = link_element['href'] if link_element and 'href' in link_element.attrs else "N/A"

            # Extract the summary (from sibling or associated element)
            subtitle_element = article.find_next_sibling('div', class_='slotSubTitle')
            subtitle_span = subtitle_element.find('span') if subtitle_element else None
            summary = subtitle_span.text.strip() if subtitle_span else "N/A"

            # Use current datetime since no timestamp element is provided in the example
            datetime_value = datetime.now().isoformat()

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
