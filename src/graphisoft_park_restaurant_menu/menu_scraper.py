from collections import defaultdict
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

MENU_URL = "https://arco-s.com"


@dataclass
class Category:
    name: str
    dishes: list


def _sort_categories(categories: list[Category]) -> list[Category]:
    category_order = [
        "Levesek",
        "Egytálételek",
        "Frissensültek",
        "Köretek",
        "Halak",
        "Desszert",
    ]
    category_order = {name: index for index, name in enumerate(category_order)}

    sorted_categories = sorted(
        categories, key=lambda c: category_order.get(c.name, float("inf"))
    )
    return sorted_categories


def scrape_menu() -> list[Category]:
    response = requests.get(MENU_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    menu = defaultdict(list)
    current_category = "Kategorizálatlan"
    elements = soup.find_all(["div", "ul"], class_=["felirat", "products"])
    for elem in elements:
        if "felirat" in elem.get("class", []):
            # Extract the category name
            current_category = elem.get_text(strip=True).capitalize()
        elif "products" in elem.get("class", []):
            # Find all product titles within the current category
            titles = elem.find_all("h2", class_="woocommerce-loop-product__title")
            for title in titles:
                menu[current_category].append(title.get_text(strip=True))

    return _sort_categories(
        [Category(name=cat, dishes=dishes) for cat, dishes in menu.items()]
    )


if __name__ == "__main__":
    result = scrape_menu()

    for category, dishes in result.items():
        print(f"--- {category} ---")
        for dish in dishes:
            print(f"  • {dish}")
