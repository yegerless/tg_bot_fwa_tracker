import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from config import BOT_TOKEN
from handlers.base_handlers import base_router
from handlers.profile import profile_router
from handlers.tracker import tracker_router

logger.add("logs.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO", rotation="100 MB")



async def main():
    ''' Написать докстрингу '''
    
    # Логгирование при запуске бота
    logger.info('The bot has STARTED')
    
    bot = Bot(token=BOT_TOKEN)
    
    # Диспетчер, на который вешаются роутеры и мидлварь для логгирования
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_routers(base_router, profile_router, tracker_router)
    
    # тут повесить мидлварь для логгирования
    
    # Пропуск всех накопленных входящих сообщений при запуске бота
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запуск бота
    await dp.start_polling(bot)
    
    logger.info('The bot has STOPPED')
    


if __name__ == '__main__':
    asyncio.run(main())
