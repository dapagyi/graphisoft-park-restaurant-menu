import os

import structlog
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from graphisoft_park_restaurant_menu.menu_scraper import scrape_menu
from graphisoft_park_restaurant_menu.notification import send_menu_to_slack

load_dotenv()
log = structlog.get_logger()


def main() -> None:
    is_slack_configured = (
        True if (os.getenv("SLACK_BOT_TOKEN") and os.getenv("SLACK_CHANNEL")) else False
    )

    if not is_slack_configured:
        log.warning(
            "Slack configuration is missing. Notifications will not be sent to Slack."
        )

    timezone = os.getenv("TIMEZONE", "Europe/Budapest")
    scheduler = BlockingScheduler(timezone=timezone)
    trigger = CronTrigger.from_crontab(
        os.getenv("NOTIFICATION_SCHEDULE", "0 11 * * mon-fri")
    )

    @scheduler.scheduled_job(trigger)
    def _send_menu_to_slack_job() -> None:
        try:
            menu = scrape_menu()
            log.debug("Menu scraped successfully", menu=menu)
            if is_slack_configured:
                response = send_menu_to_slack(menu)
                log.debug(
                    "Menu sent to Slack successfully", response_data=response.data
                )

        except Exception as e:
            log.error("Error occurred while scraping menu", error=e)

    try:
        log.info(
            "Starting scheduler with trigger: %s",
            trigger,
            timezone=timezone,
            is_slack_configured=is_slack_configured,
        )
        scheduler.start()
    except KeyboardInterrupt:
        log.info("Stopping scheduler")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
