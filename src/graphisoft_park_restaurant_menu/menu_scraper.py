from collections import defaultdict

import requests
from bs4 import BeautifulSoup

MENU_URL = "https://arco-s.com"


def scrape_menu() -> dict:
    response = requests.get(MENU_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    menu = defaultdict(list)
    current_category = "Kategorizálatlan"
    elements = soup.find_all(["div", "ul"], class_=["felirat", "products"])
    for elem in elements:
        if "felirat" in elem.get("class", []):
            # Extract the category name
            current_category = elem.get_text(strip=True)
        elif "products" in elem.get("class", []):
            # Find all product titles within the current category
            titles = elem.find_all("h2", class_="woocommerce-loop-product__title")
            for title in titles:
                menu[current_category].append(title.get_text(strip=True))

    return menu


if __name__ == "__main__":
    result = scrape_menu()

    for category, dishes in result.items():
        print(f"--- {category} ---")
        for dish in dishes:
            print(f"  • {dish}")
