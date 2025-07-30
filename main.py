from app.config import AppConfig
from app.use_cases.send_notification import SendNotificationUseCase

def main():
    cfg = AppConfig("config.json")
    use_case = SendNotificationUseCase(cfg)
    status = use_case.execute(
        message="Backup completed successfully ✅",
        title="Backup Status",
        extra_headers={"tags": "backup,success"}
    )
    print(f"Notification sent, status code: {status}")

if __name__ == "__main__":
    main()