from aiogram import types, Dispatcher
from config import bot, dp, ADMIN
import random

async def echo(message: types.Message):
    if message.from_user.id != ADMIN:
        await message.reply("Ты не мой admin!")
    else:
        if message.text.lower() == "game":
            a = ['⚽️','🏀','🎲','🎯','🎳','🎰']
            await bot.send_dice(message.chat.id, emoji=random.choice(a))

def register_hendler_extra(dp: Dispatcher):
    dp.register_message_handler(echo)