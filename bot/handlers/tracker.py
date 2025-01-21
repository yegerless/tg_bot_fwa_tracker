from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from storage import storage
from middleware.middleware import LoguruMiddleware
from utils.utils import get_food_calories, get_workout, get_additional_water


# Содание роутера и прикрепление к нему логгера
tracker_router = Router()
tracker_router.message.middleware(LoguruMiddleware(router_name='profile_router'))



class LogFood(StatesGroup):
    '''Класс группа состояний для конечного автомата по логированию еды'''
    
    input_food_quantity = State()


@tracker_router.message(Command('check_progress'))
async def check_progress(message: Message):
    '''
        Обработчик команды '/check_progress'.
        Возвращает информационное сообщение с прогрессом 
            пользователя по воде и калориям.
    '''

    date = datetime.today().strftime('%d-%m-%Y')

    # Получени данных пользователя из хранилища по id
    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if user_data:
        # Только сегодняшние данные иначе ноль
        logged_water = user_data.get('logged_water').get(date, 0)
        logged_calories = user_data.get('logged_calories').get(date, 0)
        burned_calories = user_data.get('burned_calories').get(date, 0)

        # Только если данные были введены сегодня хотя бы раз
        if logged_water:
            logged_water = sum(logged_water.values())
        if logged_calories:
            logged_calories = sum(logged_calories.values())
        if burned_calories:
            burned_calories = sum(burned_calories.values())

        # Отправка сообщения с прогрессом
        await message.answer(
            text=('Прогресс:'
                  '\n  Вода:'
                  f'\n    - Выпито: {logged_water} мл из {user_data.get('water_goal')} мл.'
                  f'\n    - Осталось: {user_data.get('water_goal') - logged_water} мл.'
                  '\n  Калории:'
                  f'\n    - Потреблено: {logged_calories} ккал из {user_data.get('calories_goal')} ккал.'
                  f'\n    - Сожжено: {burned_calories} ккал.'
                  f'\n    - Осталось: {user_data.get('calories_goal') - logged_calories} ккал.')
            )
    else:
        # Если профиля пользователя нет в хранилище, то предлагаем создать профиль
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')


@tracker_router.message(Command('log_water'))
async def log_water(message: Message, command: CommandObject):
    '''
        Обработчик команды '/log_water'.
        Принимает аргумент команды - количество выпитой 
            воды в мл и валидирует его.
        При неудачной валидации запрашивает количество воды 
            еще раз, при успешной валидации делает запись о 
            выпитой воде в хранилище.
    '''

    # Получение данных пользователя из хранилища по id
    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if not user_data:
        # Если профиля пользователя нет в хранилище, то предлагаем создать профиль
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    # Валидация полученного значения кол-ва воды
    try:
        water = int(command.args)
    except (ValueError, TypeError):
        await message.answer(text=('Вы ввели некорректное количество воды, '
                                   'пожалуйста повторите команду /log_water <кол-во выпитой воды в мл>.')
                            )
        return None

    # Логгирование воды по дате и времени
    date, time = datetime.today().strftime('%d-%m-%Y %H:%M:%S').split()
    if not user_data['logged_water'].get(date):
        user_data['logged_water'][date] = {time: water}
    else:
        user_data['logged_water'][date][time] = water

    # Проверка достиг и пользователь цели по воде и отправка соответствующего
    # сценарию сообщения
    total_water = sum(user_data['logged_water'][date].values())
    if total_water >= user_data['water_goal']:
        await message.answer(text=('Цель по воде выполнена!'
                                   f'\nВсего выпито за день {total_water} мл.')
                             )
    else:
        water_balance = user_data['water_goal'] - sum(user_data['logged_water'][date].values())
        await message.answer(text=f'До выполнения цели осталось {water_balance} мл.')


@tracker_router.message(StateFilter(None), Command('log_food'))
async def log_food(message: Message, command: CommandObject, state: FSMContext):
    '''
        Обработчик команды '/log_food'.
        Принимает аргумент команды - название съеденного продукта
            и запускает конечный автомат логирования еды.
        Делает запрос к Edamam API для получения калорийности по 
            переданному названию продукта. Если значение калорийности
            получить неудалось, то запрашивает название продукта еще раз.
            Если калорийность получена - устанавливает состояние
            input_food_quantity и запрашивает количество еды в граммах.
    '''

    # Получение данных пользователя из хранилища по id
    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if not user_data:
        # Если профиля пользователя нет в хранилище, то предлагаем создать профиль
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    # Получение калорийности из Edamam API
    food = command.args
    try:
        calories = await get_food_calories(food=food)
        if calories == 0:
            raise ValueError
    except (ValueError, TypeError):
        await message.answer(text=('Введенный продукт не найден.'
                                   '/nПожалуста введите название продукта еще раз '
                                   'при помощи команды /log_food <название продукта>')
                             )
        return None

    # Фиксация калорийности в хранилище автомата
    await state.update_data(food_calories=calories)
    # Запрос кол-ва еды
    await message.answer(text=f'{food.capitalize()} - {calories} ккал на 100 г. Сколько грамм вы съели?')
    await state.set_state(LogFood.input_food_quantity)


@tracker_router.message(LogFood.input_food_quantity, F.text)
async def set_food_quantity(message: Message, state: FSMContext):
    '''
        Обработчик состояния конечного автомата input_food_quantity.
        Принимает кол-во съеденного продукта в граммах и валидирует его.
        При неудачной валидации запрашивает кол-во продукта еще раз,
            при успешной валидации сбрасывает конечный автомат и
            делает запись о полученных калориях в хранилище.
    '''

    # Получение данных пользователя из хранилища по id
    user_id = message.from_user.id
    user_data = storage.get(user_id)

    # Валидация полученного значения кол-ва еды
    try:
        quantity = int(message.text)
    except (ValueError, TypeError):
        await message.answer(text='Вы ввели некорректное количество еды. Введите сколько грамм вы съели?')
        return None

    # Получение калорийности продукта из хранилища конечного автомата
    user_food = await state.get_data()
    # Расчет кол-ва полученных калорий
    total_calories = int(quantity * user_food.get('food_calories') / 100)

    # Логгирование полученных калорий по дате и времени
    date, time = datetime.today().strftime('%d-%m-%Y %H:%M:%S').split()
    if not user_data['logged_calories'].get(date):
        user_data['logged_calories'][date] = {time: total_calories}
    else:
        user_data['logged_calories'][date][time] = total_calories

    await message.answer(text=f'Записано {total_calories} ккал.')
    await state.clear()


@tracker_router.message(Command('log_workout'))
async def log_workout(message: Message, command: CommandObject):
    '''
        Обработчик команды '/log_workout'.
        Принимает два аргумента команды - название физической активности 
            (например: бег) и количество минут (например 30).
        Делает запрос к Ninja API для получения кол-ва сожженных калорий по 
            названию активности и количеству минут. Если получен корректный 
            ответ, то делает запись об активности в хранилище, если получен
            некорректный ответ или ответ не получен вообще, то запрашивает
            информацию об активности еще раз.
    '''

    # Получение данных пользователя из хранилища по id
    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if not user_data:
        # Если профиля пользователя нет в хранилище, то предлагаем создать профиль
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    # Парсинг аргументов команды (время после последнего пробела, название до последнего пробела)
    activity = ' '.join(command.args.split(' ')[:-1])
    duration = int(command.args.split(' ')[-1])
    weight = user_data.get('weight')

    # Получение кол-ва сожженных калорий и сохранение в хранилище или ошибка и повторный запрос
    try:
        burned_calories = await get_workout(activity=activity, duration=duration, weight=weight)

        # Логгирование соженных калорий по дате и времени
        date, time = datetime.today().strftime('%d-%m-%Y %H:%M:%S').split()
        if not user_data['burned_calories'].get(date):
            user_data['burned_calories'][date] = {time: burned_calories}
        else:
            user_data['burned_calories'][date][time] = burned_calories
    except (IndexError, ValueError, TypeError):
        await message.answer(text=(f'Тип тренировки "{activity}" не найден, '
                                   'пожалуйста повторите команду с корректным типом тренировки.')
                            )
        return None

    # Расчет дополнительного кол-ва воды по данным об активности
    additional_water = get_additional_water(duration)
    
    await message.answer(text=(f'{activity.capitalize()} {duration} минут - {burned_calories} ккал. '
                               f'Дополнительно выпейте {additional_water} мл воды.')
                        )
