from datetime import datetime

from utils import register_error

datetime_now = datetime.today().strftime("%Y-%m-%d")


def save_prices_file(data, item_data):
    item_name, tier, enchantment = item_data.values()

    try:
        # Guardar la respuesta en un archivo de texto
        file_path = f"media/{tier}_{enchantment}_{item_name}_{datetime_now}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)

        return file_path  # Devuelve la ruta del archivo en lugar del texto
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        register_error(f"Error al guardar el archivo: {e}")
        return None
