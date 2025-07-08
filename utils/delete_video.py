import os
import asyncio


async def delete_file(path):
    """Delete video after 3 minutes"""
    await asyncio.sleep(20)  # Esperar 20 segundos

    if os.path.exists(path):
        os.remove(path)
        print(f"file deleted in {path}")
    else:
        print(f"⚠️ No se encontró el archivo: {path}")
