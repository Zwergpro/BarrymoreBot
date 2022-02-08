from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import logging

from aiogram import Dispatcher, executor

from settings import settings


bot = Bot(token=settings.BOT_API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


async def on_start(dispatcher: Dispatcher):
    import handlers
    import house_services


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown, on_startup=on_start)
