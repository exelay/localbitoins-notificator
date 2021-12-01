from loguru import logger
from aiogram import executor

from core.handlers import dp


if __name__ == '__main__':
    logger.info('Бот запущен и готов к работе.')
    executor.start_polling(dp)
