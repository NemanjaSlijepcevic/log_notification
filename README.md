# Log Notification App

The **Log Notification** app inspects logs in the `/app/logs/` directory and checks new lines for patterns defined in the `NOTIFICATION_PATTERNS` environment variable. If a match is found, the app sends a notification via Telegram.

## Features
- Monitors log files in the `/app/logs/` directory for new lines.
- Matches new lines against a set of defined patterns (`NOTIFICATION_PATTERNS`).
- Sends notifications via Telegram when a pattern is detected.

### Default Notification Patterns:
- `WARNING`
- `EXCEPTION`
- `ERROR`
- `INFO`

You can modify these patterns by setting the `NOTIFICATION_PATTERNS` environment variable.

## Prerequisites
- Docker
- Telegram Bot API Token and Chat ID for notifications

## Deployment

### Option 1: Pull Docker Image from Docker Hub

If you prefer not to build the image yourself, you can pull the pre-built image from Docker Hub.

1. **Pull the Docker Image**:
    ```bash
    docker pull nemanjaslijepcevic/log_notification
    ```

2. **Run the Docker Container**:
    ```bash
    docker run -d \
      -e TELEGRAM_BOT_TOKEN=<your-bot-token> \
      -e TELEGRAM_CHAT_ID=<your-chat-id> \
      -e NOTIFICATION_PATTERNS=<patterns-to-notify> \
      -v /path/to/logs:/app/logs \
      nemanjaslijepcevic/log_notification
    ```

    - Replace `<your-bot-token>` with your Telegram bot's token.
    - Replace `<your-chat-id>` with the chat ID you want to send notifications to.
    - Replace `<patterns-to-notify>` with the patterns you want to monitor for in new log lines, separated by commas (e.g., `ERROR,FAILURE`).
    - The `/path/to/logs` directory on your host machine will be mounted to `/app/logs` in the container.

    To monitor multiple log files, just make sure all the log files are in the `/path/to/logs` directory on your host machine. The app will automatically monitor all `.log` files in the directory.

    Example with multiple log files:
    ```bash
    docker run -d \
      -e TELEGRAM_BOT_TOKEN=<your-bot-token> \
      -e TELEGRAM_CHAT_ID=<your-chat-id> \
      -e NOTIFICATION_PATTERNS="ERROR,WARNING,INFO,EXCEPTION" \
      -v /path/to/logs:/app/logs \
      nemanjaslijepcevic/log_notification
    ```

3. **Verify the Container is Running**:
    ```bash
    docker ps
    ```

    This will show the list of running containers. Ensure the `log_notification` container is listed.

### Option 2: Build Docker Image Locally

If you prefer to build the Docker image yourself, follow these steps:

1. **Build the Docker Image**:
    ```bash
    docker build -t log_notification .
    ```

2. **Run the Docker Container**:
    ```bash
    docker run -d \
      -e TELEGRAM_BOT_TOKEN=<your-bot-token> \
      -e TELEGRAM_CHAT_ID=<your-chat-id> \
      -e NOTIFICATION_PATTERNS=<patterns-to-notify> \
      -v /path/to/logs:/app/logs \
      log_notification
    ```

    - Replace `<your-bot-token>` with your Telegram bot's token.
    - Replace `<your-chat-id>` with the chat ID you want to send notifications to.
    - Replace `<patterns-to-notify>` with the patterns you want to monitor for in new log lines, separated by commas (e.g., `ERROR,FAILURE`).
    - The `/path/to/logs` directory on your host machine will be mounted to `/app/logs` in the container.

3. **Verify the Container is Running**:
    ```bash
    docker ps
    ```

    This will show the list of running containers. Ensure the `log_notification` container is listed.

### Option 3: Docker Compose

Alternatively, you can deploy the app using Docker Compose.

1. **Create a `docker-compose.yml` file**:
    ```yaml
    version: '3.8'
    
    services:
      log_notification:
        build: .
        environment:
          - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
          - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
          - NOTIFICATION_PATTERNS=${NOTIFICATION_PATTERNS}
        volumes:
          - ./logs:/app/logs
        restart: always
    ```

2. **Set Environment Variables**:

    You can set the required environment variables in a `.env` file:

    ```bash
    TELEGRAM_BOT_TOKEN=<your-bot-token>
    TELEGRAM_CHAT_ID=<your-chat-id>
    NOTIFICATION_PATTERNS=<patterns-to-notify>
    ```

    Or, export them in your terminal session:

    ```bash
    export TELEGRAM_BOT_TOKEN=<your-bot-token>
    export TELEGRAM_CHAT_ID=<your-chat-id>
    export NOTIFICATION_PATTERNS=<patterns-to-notify>
    ```

3. **Start the App with Docker Compose**:
    ```bash
    docker-compose up -d
    ```

    This will build and start the container in detached mode.

4. **Verify the Service**:
    ```bash
    docker-compose ps
    ```

    You can check the logs for troubleshooting:
    ```bash
    docker-compose logs
    ```

### Stopping the App

To stop the app running in Docker Compose, run:
```bash
docker-compose down
```

In Docker:
```bash
docker stop <container-id>
```

## Logs Directory

Make sure the logs are accessible in the `/app/logs/` directory within the container. You can map this to a directory on your host machine to provide log files to the app. 

For example, to map logs from your host system to the container:

```bash
-v /path/to/logs:/app/logs
```

The app will monitor all `.log` files inside the `/app/logs/` directory.

## Telegram Configuration

To enable Telegram notifications:
1. **Create a Telegram bot** using [BotFather](https://core.telegram.org/bots#botfather).
2. **Get your bot token** and **chat ID**.
   - For the chat ID, you can use [this tool](https://api.telegram.org/bot<your-bot-token>/getUpdates) or send a message to your bot and use the Telegram API to retrieve the chat ID.
3. Set the following environment variables in your Docker container or Docker Compose file:
    - `TELEGRAM_BOT_TOKEN`: Your bot token.
    - `TELEGRAM_CHAT_ID`: Your chat ID.
    - `NOTIFICATION_PATTERNS`: Comma-separated list of patterns to match in log lines. Default patterns are `WARNING, EXCEPTION, ERROR, INFO`.

## Example Usage

1. The app will monitor the logs directory for new lines in log files.
2. If any of the defined patterns are found in a new line, a notification is sent to the specified Telegram chat.

For example, if the `NOTIFICATION_PATTERNS` are set to `ERROR,FAILURE`, the app will monitor new lines in the log files and send a Telegram notification if any of the lines contain "ERROR" or "FAILURE".

## Troubleshooting

- Ensure that the bot token and chat ID are correct.
- Check if the log directory is correctly mounted.
- Check the logs of the running container for any issues:
    ```bash
    docker-compose logs
    ```
