import os
import asyncio

from utils.logger import logger


async def delete_file(path):
    """Delete video after 3 minutes"""
    await asyncio.sleep(20)

    if os.path.exists(path):
        os.remove(path)
        logger.info("File deleted", path=path)
    else:
        logger.warning("File not found for deletion", path=path)