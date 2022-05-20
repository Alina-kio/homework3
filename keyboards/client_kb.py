from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mem_button = KeyboardButton("/mem")
quiz_button = KeyboardButton("/quiz")
register_button = KeyboardButton("/register")

start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

start_markup.row(mem_button, quiz_button, register_button)


cancel_button = KeyboardButton('CANCEL')
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

start_markup.add(cancel_button)