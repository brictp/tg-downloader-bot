import re
from aiogram.types import Message, FSInputFile

from utils import download_video, register_error, delete_video, albion_request


class BotHandlers:
    def __init__(self):
        """Inicializa la clase con la instancia del bot"""

    async def start_bot(self, message: Message):
        """Comando /start"""
        print("hello i started")
        await message.reply("hellow")

    async def get_group_id(self, message: Message):
        """Obtener ID del grupo"""
        print("hello i started idgrupo")

        if message.chat.type in ("group", "supergroup"):
            chat_id = message.chat.id
            await message.reply(f"Group id: {chat_id}")
        elif message.chat.type == "private":
            await message.reply("This command only works in groups")
        else:
            await message.reply("Cannot determine the type of chat")

    async def search_and_download(self, message: Message):
        """Buscar URL en mensaje y descargar video"""
        url_pattern = r"https?://[^\s]+"
        urls = re.findall(url_pattern, message.text)

        if urls:
            url = urls[0]
            status_message = await message.reply(
                "🔄 Descargando el video, esto puede tardar unos momentos..."
            )

            try:
                # Descargar el video
                path_to_video = download_video(url)

                # Subir el video al grupo de Telegram
                video_file = FSInputFile(path_to_video)
                await message.bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    caption="🎥 Aquí está tu video.",
                )

                delete_video(path_to_video)

            except Exception as e:
                await message.reply("Error descargando video")
                print(f"error: {e}")
                register_error(e)

            await status_message.delete()

    async def get_albion_price(self, message: Message):
        """Obtener el precio de un objeto en Albion Online"""
        # Extraer el comando y los argumentos del mensaje
        try:
            command, args = message.text.split(" ", 1)
        except ValueError:
            await message.reply(
                "❌ Debes proporcionar el nombre del objeto y su nivel. Ejemplo: /price item 5.3"
            )
            return

        status_message = await message.reply("🔄 Buscando el precio del objeto...")

        # Procesar los argumentos
        try:
            item_name, tier_enchantment = args.split(" ", 1)
            tier, enchantment = tier_enchantment.split(".")
        except ValueError:
            await status_message.delete()
            await message.reply("❌ Formato incorrecto. Ejemplo: /price item 5.3")
            return

        # Determinar si el objeto es de refinar o refinado
        refining_items = [
            "hide",
            "ore",
            "metalbar",
            "leather",
            "wood",
            "rock",
            "planks",
            "cloth",
            "fiber",
            "stone",
        ]

        if any(refining_item in item_name for refining_item in refining_items):
            item = f"T{tier}_{item_name.upper()}_LEVEL{enchantment}@{enchantment}"
        else:
            item = f"T{tier}_{item_name}@{enchantment}"

        # Construir el enlace
        host = "https://west.albion-online-data.com"
        next = f"/api/v2/stats/charts/{item}.json?time-scale=1"
        LINK = f"{host}{next}"

        # Obtener los datos y organizar por ciudad y calidad
        data = albion_request.fetch_data(LINK)
        await status_message.delete()
        if data:
            response = albion_request.build_response(data)
            await message.reply(response)
        else:
            await message.reply("❌ No se pudo obtener la información del objeto.")
