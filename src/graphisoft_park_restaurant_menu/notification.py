import os

from dotenv import load_dotenv
from slack_sdk import WebClient

from graphisoft_park_restaurant_menu.menu_scraper import scrape_menu

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]


def build_slack_message(menu):
    lines = []
    for category in menu:
        lines.append(f"_{category}_")
        for item in menu[category]:
            lines.append(f"   • {item}")
        lines.append("")

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join(lines),
            },
        }
    ]


def send_menu_to_slack(menu):
    blocks = build_slack_message(menu)
    print(blocks)

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
