from environs import Env


env = Env()
env.read_env()

# Telegram Bot Token
TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN')

# Local Bitcoins Keys
HMAC_KEY = env.str('HMAC_KEY')
HMAC_SECRET = env.str('HMAC_SECRET')

AVAILABLE_USERS = (305516197, )
