# Telegram Bot

docker build -t telegram_bot:v1 .
docker run -d --name telegram_bot_container telegram_bot:v1

docker rm telegram_bot_container