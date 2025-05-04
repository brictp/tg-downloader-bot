import re
from aiogram.types import Message, FSInputFile


from utils import (
    fetch_data,
    build_response,
    parse_item_info,
    create_prices_file,
    build_link_price,
    download_video,
    register_error,
    delete_file,
)


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

                delete_file(path_to_video)

            except Exception as e:
                await message.reply("Error descargando video")
                print(f"error: {e}")
                register_error(e)

            await status_message.delete()

    async def get_albion_price(self, message: Message):
        """Obtener el precio de un objeto en Albion Online"""

        # Extraer el comando y los argumentos del mensaje
        item_data = await parse_item_info.parse_item_info(message)

        status_message = await message.reply(
            "🔄 Buscando el precio del objeto, esto puede tardar unos momentos..."
        )

        LINK = await build_link_price.build_link_price(item_data)

        # Obtener los datos y organizar por ciudad y calidad
        data = fetch_data.fetch_data(LINK)
        await status_message.delete()

        # Verificar si se obtuvo información
        if data:
            response = build_response.build_response(data)

            try:
                if len(response) > 1500:
                    new_prices_file = create_prices_file.save_prices_file(
                        response, item_data
                    )

                    document = FSInputFile(new_prices_file)
                    await message.reply_document(document)

                    delete_file(new_prices_file)
                else:
                    await message.reply(response)

            except Exception as e:
                await message.reply("❌ Error al enviar la respuesta.")
                print(f"Error al enviar la respuesta: {e}")
                register_error(f"Error al enviar la respuesta: {e}")
        else:
            await message.reply("❌ No se pudo obtener la información del objeto.")
