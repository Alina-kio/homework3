from aiogram import types, Dispatcher
from config import bot, dp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from keyboards import client_kb


async def start(message: types.Message):
    await message.answer(f"Hi, my friend {message.from_user.full_name}",
                         reply_markup=client_kb.start_markup)

async def pic(message: types.Message):
    photo = open("media/mem.jpg", 'rb')
    await bot.send_photo(message.from_user.id, photo=photo)



async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data="button_call_1")
    markup.add(button_call_1)
    question = 'Когда появился термин «информационные технологии» в современном значении?'
    answers = ['В 1893 году', 'В 1990 году', 'В 1958 году']
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Да, это не так легко",
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(pic, commands=['mem'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
