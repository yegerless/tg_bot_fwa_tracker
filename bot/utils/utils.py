import aiohttp
from loguru import logger
from googletrans import Translator

from config import OW_API_KEY, NINJAS_API_KEY, EDAMAM_APP_ID, EDAMAM_API_KEY


# Добавление обработчика с сохранением логов бота в файл с ротацией по размеру файла
logger.add("logs.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", 
           level="INFO", rotation="100 MB")


async def get_city_temp(city: str) -> float | None:
    '''
        Функция get_city_temp - принимает название города и возвращет
            текущую температуру в городе из OpenWeather API.
        Аргументы:
            city (str) - название города.
    '''

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OW_API_KEY}&units=metric'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                current_temp = await response.json()
                logger.info(f'Success request to OpenWeather API with city={city}')
                return current_temp.get('main').get('temp')
            else:
                logger.error(f'OpenWeather API return code {response.status} and message {await response.text()}')
            return None


def get_water_norm(weight: float, activity: int, city_temp: float = 0) -> int:
    '''
        Функция get_water_norm - принимает вес, уровень физ активности и температуру 
            в городе проживания пользователя, возвращает рассчетную цель по воде 
            для пользователя.
        Аргументы:
            weight (float) - вес пользователя в кг.
            activity (int) - физическая активность пользователя (мин/день). 
            city_temp (float) - температура в городе проживания, по дефолту 0.
    '''

    water_norm = int(weight * 30 + activity / 30 * 500 + [0, 500][city_temp > 25])
    return water_norm


def get_kallories_norm(weight: float, height: int, age: int, activity: int = 0) -> int:
    '''
        Функция get_kallories_norm - принимает вес, рост, возраст и уровень физ 
            активности пользователя, возвращает рассчетную цель по калориям 
            для пользователя.
        Аргументы:
            weight (float) - вес пользователя в кг.
            height (int) - рост пользователя в см.
            age (int) - возраст пользователя в полных годах
            activity (int) - физическая активность пользователя (мин/день),
                по дефолту 0.
    '''

    kallories_norm = int(10 * weight + 6.25 * height - 5 * age + 5 * activity)
    return kallories_norm


async def get_food_calories(food: str) -> int:
    '''
        Функция get_food_calories - принимает название продукта и возвращает 
            его калорийность на 100 г по данным из Edamam API.
        Аргументы:
            food (str) - название продукта.
    '''

    # Перевод названия продукта на английский язык для запроса к Edamam API
    async with Translator() as translator:
        food = await translator.translate(food)
        food = food.text + ' 100g'

    url = f'https://api.edamam.com/api/nutrition-data'
    params = {'app_id': EDAMAM_APP_ID, 'app_key': EDAMAM_API_KEY, 
              'nutrition-type': 'logging', 'ingr': food}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                calories = await response.json()
                logger.info(f'Success request to Edamam API with food={food}')
                return int(calories.get('calories'))
            else:
                logger.error(f'Edamam API return code {response.status} and message {await response.text()}')
            return None


async def get_workout(activity: str, duration: int, weight: int = 70) -> int:
    '''
        Функция get_workout - принимает название и длительность физической активности, а 
            также вес пользователя, возвращает значение кол-ва сожженных калорий по
            данным из Ninjas API.
        Аргументы:
            activity (str) - название физической активности.
            duration (int) - длительность физической активности.
            weight (int) - вес пользователя (по дефолту 70).
    '''

    # Перевод названия продукта на английский язык для запроса к Ninjas API
    async with Translator() as translator:
        activity = await translator.translate(activity)
        activity = activity.text

    # Пересчет килограммов в фунты для запроса к Ninjas API
    weight = weight * 2.205

    url = f'https://api.api-ninjas.com/v1/caloriesburned?activity={activity}&weight={weight}&duration={duration}'
    headers = {'X-Api-Key': NINJAS_API_KEY}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                workout = await response.json()
                logger.info(f'Success request to Ninjas API with activity={activity}')
                return int(workout[0].get('total_calories'))
            else:
                logger.error(f'Ninjas API return code {response.status} and message {await response.text()}')
            return None


def get_additional_water(activity_duration: int) -> int:
    '''
        Функция get_additional_water - принимает длительность физической активности
            и возвращает рассчетное значение кол-ва воды, которую пользователь должен
            выпить дополнительно к дневной цели.
        Аргументы:
            activity_duration (int) - длительность физической активности в минутах.
    '''

    additional_water = int(activity_duration / 30 * 200)
    return additional_water
