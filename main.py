import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.handlers import router, cleanup_old_entries
from cache_updating import run_update_cache

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    asyncio.create_task(cleanup_old_entries())
    asyncio.create_task(run_update_cache())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
