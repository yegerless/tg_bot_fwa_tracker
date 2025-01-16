from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message


base_router = Router()


@base_router.message(Command('start'))
async def cmd_start(message: Message):
    ''' Тут пропишем докстрингу '''
    
    # Пока нет мидлвари с логгером будем дебажить бота принтами
    print('Trigger command start handler')
    
    with open('bot/static/start.md', 'r') as file:
        answer_text = file.read()
    
    await message.answer(text=answer_text)
