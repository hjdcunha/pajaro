import logging
import schedule
import time
from datetime import datetime
from app.config import AppConfig
from app.use_cases.send_notification import SendNotificationUseCase
import nvdlib

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_latest_cve():
    """Fetches the latest CVE from the NVD."""
    try:
        # Define the date range for the past 24 hours
        end_date = datetime.utcnow()
        start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Fetch CVEs published within the last 24 hours
        cves = nvdlib.searchCVE(pubStartDate=start_date, pubEndDate=end_date, limit=1)
        if cves:
            logger.info(f"Fetched latest CVE: {cves[0].id}")
            return cves[0]
        else:
            logger.warning("No CVEs found in the specified date range.")
            return None
    except Exception as e:
        logger.error(f"Failed to fetch latest CVE: {e}")
        return None

def send_notification():
    """Fetches the latest CVE and sends a notification."""
    # Fetch the latest CVE
    latest_cve = fetch_latest_cve()

    if latest_cve:
        # Prepare the message and title
        message = f"Latest CVE: {latest_cve.id}\nDescription: {latest_cve.descriptions[0] if latest_cve.descriptions else 'No description available.'}"
        title = f"CVE-{latest_cve.id}"

        # Initialize configuration and use case
        cfg = AppConfig("config.json")
        use_case = SendNotificationUseCase(cfg)

        # Send the notification
        status = use_case.execute(
            message=message,
            title=title,
            extra_headers={"tags": "security,cve"}
        )
        logger.info(f"Notification sent, status code: {status}")
    else:
        logger.error("No CVE fetched, notification not sent.")

# Schedule the task to run every hour
schedule.every().hour.at(":05").do(send_notification)

while True:
    schedule.run_pending()
    time.sleep(1)