from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from loguru import logger

# Добавление обработчика с сохранением логов бота в файл с ротацией по размеру файла
logger.add("logs.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", 
           level="INFO", rotation="100 MB")



class LoguruMiddleware(BaseMiddleware):
    '''
        Мидлварь, которая логгирует все полученные от пользователя сообщения,
        которые были обработаны хэндлерами.
    '''

    def __init__(self, router_name: str | None = None):
        '''
            Конструктор экземпляров мидлвари. 
            Принимает аргумент router_name - имя роутера, на который 
                добавляется экземпляр мидлвари.

            Прим.: это имитация легаси кода в проекте, на самом деле
                функционал мидлвари, для которого нужно было имя роутера,
                я выпилил еще в середине работы, а про этот конструктор 
                вспомнил только в самом конце...
        '''

        self.router_name = router_name


    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        ''' 
            Метод __call__ реализует возможность экземпляров  мидлвари быть вызванными
                как функция.
            Здесь реализован функционал логгирования пойманных сообщений.
        '''

        # Логгирование момента получения сообщения и отправки ответа
        if data.get('command'):
            logger.info(f'Message received {data.get('command').command}')
        else:
            logger.info(f'Message received {data.get('event_update').message.text}')
        result = await handler(event, data)
        return result