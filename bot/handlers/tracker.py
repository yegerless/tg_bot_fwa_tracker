from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command, CommandObject

from storage import storage
from middleware.middleware import LoguruMiddleware
from utils.utils import get_food_kalories


tracker_router = Router()
tracker_router.message.middleware(LoguruMiddleware(router_name='profile_router'))


@tracker_router.message(Command('check_progress'))
async def check_progress(message: Message):
    ''' Докстринга '''

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if user_data:
        await message.answer(text=f'''Прогресс: 
                                Вода: 
                                    - Выпито: {0} мл из {user_data.get('water_goal')} мл.
                                    - Осталось: {user_data.get('water_goal') - 0} мл.
                                
                                Калории:
                                    - Потреблено: {0} ккал из {user_data.get('water_goal')} ккал.
                                    - Сожжено: {0} ккал.
                                    - Осталось: {user_data.get('kalories_goal') - 0} ккал.
                            ''')
    else:
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')


@tracker_router.message(Command('log_water'))
async def log_water(message: Message, command: CommandObject):
    ''' Докстринга '''

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if not user_data:
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    try:
        water = int(command.args)
    except (ValueError, TypeError):
        await message.answer(text='Вы ввели некорректное количество воды, пожалуйста повторите команду /log_water <кол-во выпитой воды в мл>')
        return None

    # Логгирование воды будет с точностью до секунд
    date, time = datetime.today().strftime('%d-%m-%Y %H:%M:%S').split()
    if not user_data['logged_water'].get(date):
        user_data['logged_water'][date] = {time: water}
    else:
        user_data['logged_water'][date][time] = water

    water_balance = user_data['water_goal'] - sum(user_data['logged_water'][date].values())
    await message.answer(text=f'До выполнения цели осталось {water_balance}')


@tracker_router.message(Command('log_food'))
async def log_food(message: Message, command: CommandObject):
    ''' Докстринга '''

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    food = command.args
    print(food)
    kalories = await get_food_kalories(food=food)
    await message.answer(text=f'{kalories}')


@tracker_router.message(Command('log_workout'))
async def log_workout(message: Message, command: CommandObject):
    ''' Докстринга '''

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    pass