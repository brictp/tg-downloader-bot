import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def register_error(error_message):
    """Registra errores en el archivo logs/errors.log"""
    logging.error(error_message)
