# Telegram Bot

docker build -t telegram_bot:latest .
docker run -d --name telegram_bot_container telegram_bot:latest

docker rm telegram_bot_container