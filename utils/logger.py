import logging
import os
import sys

# --- Configuración (solo se ejecuta una vez) ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# ------------------------------------------------


def register_error(error_message):
    """Registra errores en el archivo logs/errors.log.
    El mensaje de error se registra en una SOLA línea
    porque no incluimos el traceback."""

    # Esta línea siempre generará una entrada de log de una sola línea
    # (asctime - ERROR - error_message), a menos que 'error_message'
    # contenga saltos de línea.
    logging.error(error_message)
