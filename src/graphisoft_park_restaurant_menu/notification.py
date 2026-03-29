import os
from pprint import pprint

from dotenv import load_dotenv
from slack_sdk import WebClient

from graphisoft_park_restaurant_menu.menu_scraper import scrape_menu

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]


def build_slack_message(menu: dict) -> list:
    category_fields = []
    for category, dishes in menu.items():
        dishes_markdown = "\n".join(f"   • {dish}" for dish in dishes)
        category_fields.append(
            {"type": "mrkdwn", "text": f"*{category}*\n{dishes_markdown}"}
        )

    return [
        {
            "type": "section",
            "fields": category_fields,
        },
    ]


def send_menu_to_slack(menu: dict) -> None:
    blocks = build_slack_message(menu)
    pprint(blocks)

    client = WebClient(token=SLACK_BOT_TOKEN)
    client.chat_postMessage(
        channel=SLACK_CHANNEL,
        blocks=blocks,
        username="Kör Étterem",
        icon_emoji="fork_and_knife",
        text="Check out today's menu!",
    )


if __name__ == "__main__":
    menu = scrape_menu()
    send_menu_to_slack(menu)
