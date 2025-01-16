from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from loguru import logger

logger.add("logs.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO", rotation="100 MB")



class LoguruMiddleware(BaseMiddleware):
    ''' Докстринга '''

    def __init__(self, router_name: str | None = None):
        ''' Докстринга '''
        
        self.router_name = router_name


    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        ''' Докстринга '''
        
        # Логгирование момента получения сообщения и отправки ответа
        logger.info(f'Message received in router {self.router_name}')
        result = await handler(event, data)
        logger.info(f'The handler from router {self.router_name} sent a response')
        return result