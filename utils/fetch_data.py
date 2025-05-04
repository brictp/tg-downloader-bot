import requests

from utils import register_error


# Función para obtener los datos
def fetch_data(link):
    try:
        res = requests.get(link)
        res.raise_for_status()  # Lanza una excepción si la respuesta no es 200 OK

        data = res.json()
        DataExport = []

        for item in data:
            location = item.get("location")
            item_id = item.get("item_id")
            quality = item.get("quality")
            prices_avg = item.get("data", {}).get("prices_avg", [])[:5]
            timestamps = item.get("data", {}).get("timestamps", [])[:5]
            item_timestamp = [timestamps[0]] if len(timestamps) > 0 else []
            if len(timestamps) > 4:
                item_timestamp.append(timestamps[4])

            data_item = {
                "item_id": item_id,
                "location": location,
                "quality": quality,
                "prices_avg": prices_avg,
                "item_timestamp": item_timestamp,
            }

            DataExport.append(data_item)

        return DataExport

    except Exception as e:
        print(f"Error fetching data {e} \n")
        register_error(f"Error fetching data {e} \n")
        return None
