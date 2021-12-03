from loguru import logger
from environs import Env


env = Env()
env.read_env()

# Logging settings
logger.add('debug.log', format="{time} {level} {message}", level="DEBUG", rotation='100 KB', compression='zip')

# Telegram Bot Token
TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN')

# Local Bitcoins Keys
HMAC_KEY = env.str('HMAC_KEY')
HMAC_SECRET = env.str('HMAC_SECRET')

ALLOWED_USERS = env.list('ALLOWED_USERS')
ALLOWED_USERS = list(map(int, ALLOWED_USERS))


