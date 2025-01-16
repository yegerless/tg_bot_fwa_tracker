from functools import wraps
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from middleware.middleware import LoguruMiddleware


base_router = Router()
base_router.message.middleware(LoguruMiddleware(router_name='base_router'))

@wraps
@base_router.message(Command('start'))
async def cmd_start(message: Message):
    ''' Тут пропишем докстрингу '''

    with open('bot/static/start.md', 'r') as file:
        answer_text = file.read()
        
    await message.answer(text=answer_text)
