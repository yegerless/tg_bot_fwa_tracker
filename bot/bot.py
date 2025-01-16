import asyncio
# import loguru
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
# from middleware import 
# from handlers import 



async def main():
    # тут сделать логгирование при запуске бота
    
    bot = Bot(token=BOT_TOKEN)
    
    # Диспетчер, на который вешаются роутеры и мидлварь для логгирования
    dp = Dispatcher(storage=MemoryStorage())
    
    # dp.include_routers()
    
    # тут повесить мидлварь для логгирования
    
    
    # Пропуск всех накопленных входящих сообщений при запуске бота
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
