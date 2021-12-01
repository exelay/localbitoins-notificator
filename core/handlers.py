from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart

from core.loader import dp
from core.settings import ALLOWED_USERS


@dp.message_handler(CommandStart())
async def start_command_handler(message: Message):
    user_id = message.from_user.id
    if user_id in ALLOWED_USERS:
        await message.answer('Теперь сюда будут приходить уведомления с Local Bitcoins.')
    else:
        await message.answer('Ты не подключен к боту, обратись к админу.')
