from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from storage import storage
from middleware.middleware import LoguruMiddleware
from utils.utils import get_city_temp, get_water_norm, get_kallories_norm


profile_router = Router()
profile_router.message.middleware(LoguruMiddleware(router_name='profile_router'))



class CreatingProfile(StatesGroup):
    ''' Докстринга '''
    input_height = State()
    input_weight = State()
    input_age = State()
    input_activity = State()
    input_city = State()
    input_kalories_goal = State()


@profile_router.message(StateFilter(None), Command('set_profile'))
async def cmd_set_profile(message: Message, state: FSMContext):
    ''' Докстринга '''

    await message.answer(text='Введите ваш рост в см, округляя до целого (например: 176)')
    await state.set_state(CreatingProfile.input_height)


@profile_router.message(CreatingProfile.input_height, F.text)
async def input_height(message: Message, state: FSMContext):
    ''' Докстринга '''

    user_id = message.from_user.id
    try:
        height =  int(message.text)
    except (ValueError, TypeError):
        await message.answer(text='Вы ввели некорректное значение роста. Введите ваш рост в см, округляя до целого (например: 70)')
        return None

    storage[user_id] = {'height': height}
    await message.answer(text=f'Введите ваш вес в кг с точность до 0.1 (например: 60.5)')
    await state.set_state(CreatingProfile.input_weight)


@profile_router.message(CreatingProfile.input_weight, F.text)
async def input_weight(message: Message, state: FSMContext):
    ''' Докстринга '''

    user_id = message.from_user.id
    try:
        weight = float(message.text)
    except (ValueError, TypeError):
        await message.answer(text='Вы ввели некорректное значение веса. Введите ваш вес в кг с точность до 0.1 (например: 60.5)')
        return None
    storage[user_id]['weight'] = weight
    await message.answer(text=f'Напишите, сколько вам полных лет? (например: 25)')
    await state.set_state(CreatingProfile.input_age)


@profile_router.message(CreatingProfile.input_age, F.text)
async def input_age(message: Message, state: FSMContext):
    ''' Докстринга '''

    user_id = message.from_user.id
    try:
        age = int(message.text)
    except (ValueError, TypeError):
        await message.answer(text='Вы ввели некорректный возраст. Напишите, сколько вам полных лет? (например: 25)')
        return None
    storage[user_id]['age'] = age
    await message.answer(text=f'Введите ваш уровень физической активности в минутах в день (например: 60)')
    await state.set_state(CreatingProfile.input_activity)


@profile_router.message(CreatingProfile.input_activity, F.text)
async def input_activity(message: Message, state: FSMContext):
    ''' Докстринга '''

    user_id = message.from_user.id
    try:
        activity =  int(message.text)
    except (ValueError, TypeError):
        await message.answer(text='Вы ввели некорректное значение физической активности. Введите ваш уровень физической активности в минутах в день (например: 60)')
        return None
    storage[user_id]['activity'] = activity
    await message.answer(text=f'Введите название города, где вы живете (например: Москва)')
    await state.set_state(CreatingProfile.input_city)


@profile_router.message(CreatingProfile.input_city, F.text)
async def input_activity(message: Message, state: FSMContext):
    ''' Докстринга '''

    user_id = message.from_user.id
    city =  message.text
    storage[user_id]['city'] = city

    temp = await get_city_temp(city=city)
    storage[user_id]['water_goal'] = get_water_norm(weight=storage[user_id]['weight'], 
                                activity=storage[user_id]['activity'],
                                city_temp = temp)

    if not temp:
        await message.answer(text=f'Не удалось получить значение температуры для введенного названия города. Норма воды расчитана без учета температуры.')
    await message.answer(text=f'Введите вашу цель по потребляемым калориям в день (например 2500) или напишите "Рассчитать", если хотите получить автоматический расчет нормы калорий для Вас.')
    await state.set_state(CreatingProfile.input_kalories_goal)


@profile_router.message(CreatingProfile.input_kalories_goal, F.text)
async def input_kalories_goal(message: Message, state: FSMContext):
    ''' Докстринга '''

    user_id = message.from_user.id
    kalories_goal =  message.text

    if kalories_goal == 'Рассчитать':
        storage[user_id]['kalories_goal'] = get_kallories_norm(weight=storage[user_id]['weight'], 
                                        height=storage[user_id]['height'],
                                        age=storage[user_id]['age'], 
                                        activity=storage[user_id]['activity'])
    else:
        try:
            kalories_goal = int(kalories_goal)
            storage[user_id]['kalories_goal'] = kalories_goal
        except (ValueError, TypeError):
            await message.answer(text='Вы ввели некорректное значение цели по каллориям. Введите вашу цель по потребляемым калориям в день (например 2500) или напишите "Рассчитать", если хотите получить автоматический расчет нормы калорий для Вас.')
            return None

    storage[user_id]['logged_water'] = {}
    storage[user_id]['logged_calories'] = {}
    storage[user_id]['burned_calories'] = {}

    await message.answer(text=f'Ваш профиль успешно создан. Цель по воде - {storage[user_id]['water_goal']} мл в день. Цель по калориям - {storage[user_id]['kalories_goal']} ккал/день')
    await state.clear()
