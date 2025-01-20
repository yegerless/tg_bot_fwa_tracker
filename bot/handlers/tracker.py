from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from storage import storage
from middleware.middleware import LoguruMiddleware
from utils.utils import get_food_kalories, get_workout, get_additional_water


tracker_router = Router()
tracker_router.message.middleware(LoguruMiddleware(router_name='profile_router'))



class LogFood(StatesGroup):
    input_food_quantity = State()



@tracker_router.message(Command('check_progress'))
async def check_progress(message: Message):
    ''' Докстринга '''

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    date = datetime.today().strftime('%d-%m-%Y')
    if user_data:
        logged_water = user_data.get('logged_water').get(date, 0)
        logged_kalories = user_data.get('logged_calories').get(date, 0)
        burned_calories = user_data.get('burned_calories').get(date, 0)
        
        if logged_water:
            logged_water = sum(logged_water.values())
        if logged_kalories:
            logged_kalories = sum(logged_kalories.values())
        if burned_calories:
            burned_calories = sum(burned_calories.values())
        
        await message.answer(
            text=('Прогресс:'
                  '\n  Вода:'
                  f'\n    - Выпито: {logged_water} мл из {user_data.get('water_goal')} мл.'
                  f'\n    - Осталось: {user_data.get('water_goal') - logged_water} мл.'
                  '\n  Калории:'
                  f'\n    - Потреблено: {logged_kalories} ккал из {user_data.get('kalories_goal')} ккал.'
                  f'\n    - Сожжено: {burned_calories} ккал.'
                  f'\n    - Осталось: {user_data.get('kalories_goal') - logged_kalories} ккал.')
            )
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
        await message.answer(text=('Вы ввели некорректное количество воды, '
                                   'пожалуйста повторите команду /log_water <кол-во выпитой воды в мл>')
                            )
        return None

    # Логгирование воды будет с точностью до секунд
    date, time = datetime.today().strftime('%d-%m-%Y %H:%M:%S').split()
    if not user_data['logged_water'].get(date):
        user_data['logged_water'][date] = {time: water}
    else:
        user_data['logged_water'][date][time] = water

    water_balance = user_data['water_goal'] - sum(user_data['logged_water'][date].values())
    await message.answer(text=f'До выполнения цели осталось {water_balance}')


@tracker_router.message(StateFilter(None), Command('log_food'))
async def log_food(message: Message, command: CommandObject, state: FSMContext):
    ''' Докстринга '''

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if not user_data:
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    food = command.args
    kalories = await get_food_kalories(food=food)

    await state.update_data(food_kalories=kalories)
    await message.answer(text=f'{food.capitalize()} - {kalories} ккал на 100 г. Сколько грамм вы съели?')
    await state.set_state(LogFood.input_food_quantity)


@tracker_router.message(LogFood.input_food_quantity, F.text)
async def set_food_quantity(message: Message, state: FSMContext):
    ''' Докстринга '''

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if not user_data:
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    try:
        quantity = int(message.text)
    except (ValueError, TypeError):
        await message.answer(text='Вы ввели некорректное количество еды. Введите сколько грамм вы съели?')
        return None

    user_food = await state.get_data()
    total_kalories = quantity * user_food.get('food_kalories') / 100

    # Логгирование еды будет с точностью до секунд
    date, time = datetime.today().strftime('%d-%m-%Y %H:%M:%S').split()
    if not user_data['logged_calories'].get(date):
        user_data['logged_calories'][date] = {time: total_kalories}
    else:
        user_data['logged_calories'][date][time] = total_kalories

    await message.answer(text=f'Записано {total_kalories} ккал.')


@tracker_router.message(Command('log_workout'))
async def log_workout(message: Message, command: CommandObject):
    ''' Докстринга '''

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if not user_data:
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    activity = ' '.join(command.args.split(' ')[:-1])
    duration = int(command.args.split(' ')[-1])
    weight = user_data.get('weight')

    try:
        burned_kalories = await get_workout(activity=activity, duration=duration, weight=weight)

        # Логгирование соженных калорий будет с точностью до секунд
        date, time = datetime.today().strftime('%d-%m-%Y %H:%M:%S').split()
        if not user_data['burned_calories'].get(date):
            user_data['burned_calories'][date] = {time: burned_kalories}
        else:
            user_data['burned_calories'][date][time] = burned_kalories
    except IndexError:
        await message.answer(text=(f'Тип тренировки "{activity}" не найден, '
                                   'пожалуйста повторите команду с корректным типом тренировки.')
                            )
        return None

    additional_water = get_additional_water(duration)

    await message.answer(text=(f'{activity.capitalize()} {duration} минут - {burned_kalories} ккал. '
                               f'Дополнительно выпейте {additional_water} мл воды.')
                        )
