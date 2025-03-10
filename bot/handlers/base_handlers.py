from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from middleware.middleware import LoguruMiddleware

# Содание роутера и прикрепление к нему логгера
base_router = Router()
base_router.message.middleware(LoguruMiddleware(router_name='base_router'))


@base_router.message(Command('start'))
async def cmd_start(message: Message):
    '''
        Обработчик команды '/start'.
        Отправляет информационное сообщение про бота и список его команд.
    '''

    # Стартовое сообщение больше, поэтому лежит в отдельном файле
    with open('bot/static/start.md', 'r') as file:
        answer_text = file.read()

    await message.answer(text=answer_text)


@base_router.message(Command('cancel'))
@base_router.message(F.text.lower() == 'отмена')
async def cmd_cancel(message: Message, state: FSMContext):
    '''
        Обработчик команды '/cancel'.
        Отменяет заполнение формы, сбрасывает текущее состояние 
            активного конечного автомата.
    '''

    await message.answer(text='Ввод информации отменен.')
    await state.clear()
