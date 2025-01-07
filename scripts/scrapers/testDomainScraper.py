from bs4 import BeautifulSoup

def fetch_html(url, session):
    response = session.get(url)
    response.raise_for_status()
    return response.text


def parse_data(html):
    soup = BeautifulSoup(html, "html.parser")
    data = []
    for item in soup.find_all("div", class_="item"):
        title = item.find("h2").text.strip()
        price = item.find("span", class_="price").text.strip()
        data.append({"title": title, "price": price})
    return data
