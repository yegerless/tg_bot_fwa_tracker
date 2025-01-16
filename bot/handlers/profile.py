from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from middleware.middleware import LoguruMiddleware
from storage import storage


profile_router = Router()
profile_router.message.middleware(LoguruMiddleware(router_name='profile_router'))



class CreatingProfile(StatesGroup):
    ''' Докстринга '''
    input_antropometry_params = State()
    input_activity = State()
    input_city = State()



@profile_router.message(StateFilter(None), Command('set_profile'))
async def cmd_set_profile(message: Message, state: FSMContext):
    ''' Докстринга '''
    
    await message.answer(text='Введите ваш рост в кг, округляя до целого (например: 70)')
    await state.set_state(CreatingProfile.input_antropometry_params)


@profile_router.message(CreatingProfile.input_antropometry_params, F.text)
async def input_antrometry_params(message: Message, state: FSMContext):
    ''' Докстринга '''
    
    await message.answer(text=f'Введите ваш уровень физической активности в минутах в день (например: 60)')
    await state.set_state(CreatingProfile.input_activity)


@profile_router.message(CreatingProfile.input_activity, F.text)
async def input_activity(message: Message, state: FSMContext):
    ''' Докстринга '''
    
    await message.answer(text=f'Введите название города, где вы живете, на английском языке (например: Moscow)')
    await state.set_state(CreatingProfile.input_city)


@profile_router.message(CreatingProfile.input_city, F.text)
async def input_activity(message: Message, state: FSMContext):
    ''' Докстринга '''
    
    await message.answer(text=f'Вы ввели {message.text}')
    await state.clear()
