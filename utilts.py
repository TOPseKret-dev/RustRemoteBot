import logging

# Конфигурация логирования: логи сохраняются в rustbot.log
logging.basicConfig(
    filename='rustbot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def log_action(message):
    logging.info(message)
