from utils import register_error


def build_response(data):
    grouped_data = {}
    try:
        min_prices = {}
        max_prices = {}

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
            formatted_prices = [
                f"{price:,.0f}$".replace(",", ".") for price in prices_avg
            ]
            grouped_data[location][quality]["prices"].extend(formatted_prices)
            grouped_data[location][quality]["timestamps"] = timestamps

            # Actualizar precios mínimos y máximos por calidad
            if quality not in min_prices:
                min_prices[quality] = {"price": float("inf"), "location": None}
            if quality not in max_prices:
                max_prices[quality] = {"price": float("-inf"), "location": None}

            for price in prices_avg:
                if price < min_prices[quality]["price"]:
                    min_prices[quality]["price"] = price
                    min_prices[quality]["location"] = location
                if price > max_prices[quality]["price"]:
                    max_prices[quality]["price"] = price
                    max_prices[quality]["location"] = location

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
                    response += f"    ⏰ Historial: {timestamps[0]}"
                    if len(timestamps) > 1:
                        response += f" - {timestamps[1]}"
                    response += "\n"
                else:
                    response += "    ⏰ Historial: No disponible\n"

            response += "\n"

        # Agregar información de precios más económicos y más costosos por calidad
        response += "📉 Ciudades con precios más económicos por calidad:\n"
        for quality, info in min_prices.items():
            response += f"  🔖 Calidad {quality}: 📍 {info['location']} con {info['price']:,.0f}$\n".replace(
                ",", "."
            )

        response += "📈 Ciudades con precios más costosos por calidad:\n"
        for quality, info in max_prices.items():
            response += f"  🔖 Calidad {quality}: 📍 {info['location']} con {info['price']:,.0f}$\n".replace(
                ",", "."
            )

        return response

    except Exception as e:
        print(f"Error al construir la respuesta: {e}")
        register_error(f"Error al construir la respuesta: {e}")
        response = (
            "❌ Error al procesar los datos. Asegúrate de que el formato sea correcto."
        )
        return None
