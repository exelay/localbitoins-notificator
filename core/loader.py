from lb_sdk import Client

from aiogram import Bot, Dispatcher

from core.settings import TELEGRAM_TOKEN, HMAC_KEY, HMAC_SECRET


bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot)

lb_client = Client(HMAC_KEY, HMAC_SECRET)
