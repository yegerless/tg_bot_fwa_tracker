from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command

from storage import storage
from middleware.middleware import LoguruMiddleware


tracker_router = Router()
tracker_router.message.middleware(LoguruMiddleware(router_name='profile_router'))