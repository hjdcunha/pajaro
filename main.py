import logging
import schedule
import time
import os
from datetime import datetime, timedelta
from datetime import datetime
from app.config import AppConfig
from app.use_cases.send_notification import SendNotificationUseCase
import nvdlib

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

LAST_CVE_FILE = "/tmp/last_cve_id.txt"

def fetch_latest_cve():
    """Fetches the latest CVE and avoids duplicates."""
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=1)

        cves = nvdlib.searchCVE(pubStartDate=start_date, pubEndDate=end_date, limit=5)
        if not cves:
            logger.info("No new CVEs found.")
            return None

        # Read the last CVE ID
        last_id = None
        if os.path.exists(LAST_CVE_FILE):
            with open(LAST_CVE_FILE, "r") as f:
                last_id = f.read().strip()

        for cve in cves:
            if cve.id != last_id:
                # Save new last ID
                with open(LAST_CVE_FILE, "w") as f:
                    f.write(cve.id)
                logger.info(f"Fetched new CVE: {cve.id}")
                return cve

        logger.info("No new CVEs different from last run.")
        return None

    except Exception as e:
        logger.error(f"Error fetching latest CVE: {e}")
        return None

def send_notification():
    """Fetches the latest CVE and sends notifications."""
    # Fetch the latest CVE
    latest_cve = fetch_latest_cve()

    if latest_cve:
        # Initialize configuration and use case
        cfg = AppConfig("config.json")
        use_case = SendNotificationUseCase(cfg)

        # Define messages and titles
        messages = [
            {
                "title": latest_cve.id,
                "message": f"Message: {latest_cve.descriptions[0].value if latest_cve.descriptions else 'No description available.'}"
            },
            {
                "title": latest_cve.sourceIdentifier,
                "message": f"Confidentiality: {latest_cve.score[2]}"
            },
            {
                "title": "CVSS Details",
                "message": f"Integrity Impact: {latest_cve.v31integrityImpact}, Base Score: {latest_cve.v31score}"
            },
        ]

        # Send all messages
        for i, msg in enumerate(messages, start=1):
            try:
                status = use_case.execute(
                    message=msg["message"],
                    title=msg["title"],
                    extra_headers={"tags": "security,cve"}
                )
                logger.info(f"Notification {i} sent, status code: {status}")
            except Exception as e:
                logger.error(f"Failed to send notification {i}: {e}")
    else:
        logger.error("No CVE fetched, notifications not sent.")



# Uncomment to run every hour
schedule.every().hour.at(":00").do(send_notification)
while True:
    schedule.run_pending()
    time.sleep(1)