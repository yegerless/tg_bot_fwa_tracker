from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message


base_router = Router()


@base_router.message(Command('start'))
async def cmd_start(message: Message):
    ''' Тут пропишем докстрингу '''
    
    # надо возвращать в качестве ответа описание бота и микроинструкцию по использованию 
    # а не просто приветствие 
    
    # Пока нет мидлвари с логгером будем дебажить бота принтами
    print(message)
    
    await message.answer(text='Этот бот категорически приветствует вас!')
