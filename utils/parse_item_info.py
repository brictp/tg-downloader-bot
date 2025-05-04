async def parse_item_info(message):
    try:
        command, args = message.text.split(" ", 1)
    except Exception as e:
        print(f"Error al dividir el mensaje: {e}")
        await message.reply(
            "❌ Debes proporcionar el nombre del objeto y su nivel. Ejemplo: /price item 5.3"
        )
        return

    # Procesar los argumentos
    try:
        item_name, tier_enchantment = args.split(" ", 1)
        tier, enchantment = tier_enchantment.split(".")

        item_data = {
            "item_name": item_name,
            "tier": tier,
            "enchantment": enchantment,
        }

        return item_data
    except Exception as e:
        print(f"Error al procesar los argumentos: {e}")
        await message.reply("❌ Formato incorrecto. Ejemplo: /price item 5.3")
        return
