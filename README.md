# RustRemoteBot

RustRemoteBot — Telegram-бот для удалённого управления ПК с поддержкой автоматизации действий в игре Rust.

## Возможности
- Анти-AFK (имитация активности)
- Авто заход на сервер Rust
- Режим "Трейдер Валера" (режим автоматической продажи удобрений в городе)
- Управление через Telegram
- Логирование действий
- Docker-контейнеризация

## Установка
1. Установите зависимости:
```
pip install -r requirements.txt
```

2. Запустите:
```
python bot.py
```

## Docker
```
docker build -t rust-bot .
docker run -e BOT_TOKEN=your_bot_token -e CHAT_ID=your_chat_id rust-bot
```
