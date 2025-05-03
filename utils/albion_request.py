import requests


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
            item_timestamp = [timestamps[0], timestamps[4]] if timestamps else []

            data_item = {
                "item_id": item_id,
                "location": location,
                "quality": quality,
                "prices_avg": prices_avg,
                "item_timestamp": item_timestamp,
            }

            DataExport.append(data_item)

        return DataExport

    except requests.exceptions.RequestException as error:
        print(f"Error fetching data: {error}")
        return None


def build_response(data):
    grouped_data = {}
    for entry in data:
        location = entry["location"]
        quality = entry["quality"]
        prices_avg = entry["prices_avg"]
        timestamps = entry["item_timestamp"]

        if location not in grouped_data:
            grouped_data[location] = {}
        if quality not in grouped_data[location]:
            grouped_data[location][quality] = {"prices": [], "timestamps": []}

        # Formatear los precios con puntos y símbolo de dólar
        formatted_prices = [f"{price:,.0f}$".replace(",", ".") for price in prices_avg]
        grouped_data[location][quality]["prices"].extend(formatted_prices)
        grouped_data[location][quality]["timestamps"] = timestamps

    # Construir la respuesta
    response = "📊 Precios del objeto:\n"
    for location, qualities in grouped_data.items():
        response += f"📍 Ciudad: {location}\n"
        for quality, details in qualities.items():
            prices = details["prices"]
            timestamps = details["timestamps"]
            response += f"  🔖 Calidad {quality}:\n"
            response += f"    💰 Precios promedio: {prices}\n"
            if timestamps:
                response += f"    ⏰ Historial: {timestamps[0]} - {timestamps[1]}\n"

        response += "\n"

    return response
