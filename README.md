# pajaro
Unidirectional Secure Notification System

## Project Structure
'├── app/
│   ├── config.py
│   ├── domain/
│   │   └── notification.py
│   ├── infra/
│   │   └── ntfy_client.py
│   └── use_cases/
│       └── send_notification.py
├── config.json
└── main.py'

## 🔧 Technical Summary [Basic Getting Started Implementation]

- **Purpose**: Sends HTTP push notifications to an ntfy endpoint. Configuration is loaded from `config.json`.

- **Architecture**:
  - **Domain Layer**: Defines core entities and business logic.
  - **Infrastructure Layer**: Handles external communication (e.g., HTTP requests).
  - **Use Cases Layer**: Orchestrates application workflows.
  - **Configuration Layer**: Centralizes and loads application settings.

- **Key Components**:
  - **`config.py`**: Loads and parses `config.json` to provide application settings.
  - **`notification.py`**: Defines the `Notification` entity with attributes like `message`, `title`, and `headers`.
  - **`ntfy_client.py`**: Implements the `NtfyClient` class to send notifications via HTTP POST requests.
  - **`send_notification.py`**: Contains the `SendNotificationUseCase` class that coordinates the sending of notifications.
  - **`main.py`**: Entry point that initializes the application and triggers the notification sending process.

- **Configuration (`config.json`)**:
  - `ntfy_url`: Base URL of the ntfy endpoint.
  - `topic`: The topic to which notifications are sent.
  - `default_title`: Default title for notifications.
  - `headers`: Additional HTTP headers to include in requests.

- **Usage**:
  - Install dependencies: `pip install requests`
  - Configure `config.json` with appropriate values.
  - Execute the application: `python main.py`

- **Extensibility**:
  - Easily extendable to support additional features such as retry logic, logging, or integration with other notification services.