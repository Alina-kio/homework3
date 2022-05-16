from aiogram import types, Dispatcher
from config import bot, ADMIN
import random

async def ban(message: types.Message):
    if message.from_user.id != ADMIN:
        await message.reply("Ты не мой admin!")
    if not message.reply_to_message:
        await message.reply("Команда должна быть ответом на сообщение!")
    else:
        if message.text.startswith("!pin"):
            await bot.pin_chat_message(message.chat.id, message.message_id)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=["pin"], commands_prefix="!")