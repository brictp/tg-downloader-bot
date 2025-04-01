import os
import asyncio


async def delete_video(path):
    """Delete video after 3 minutes"""
    await asyncio.sleep(180)  # Esperar 3 minutos

    if os.path.exists(path):
        os.remove(path)
        print(f"video deleted in {path}")
    else:
        print(f"⚠️ No se encontró el archivo: {path}")
