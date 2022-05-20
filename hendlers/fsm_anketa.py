from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, ADMIN
from keyboards.client_kb import cancel_markup
from database import bot_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    surname = State()
    age = State()
    region = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await bot.send_message(
            message.chat.id,
            f"Hi {message.from_user.full_name}, send your photo...",
            reply_markup=cancel_markup
        )
    else:
        await message.answer('Write in private chat')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = f"@{message.from_user.username}"
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Enter name of the dish...")


async def load_name_dish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name dish'] = message.text
    await FSMAdmin.next()
    await message.answer("Enter description of the dish...")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.answer("Enter price...")


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = int(message.text)
    # await bot_db.sql_command_insert(state)
    await state.finish()
    await message.answer("You can be free)")



async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply("Регистрация отменена!")


async def delete_data(message: types.Message):
    if message.from_user.id == ADMIN:
        result = await bot_db.sql_command_all()
        for i in result:
            await bot.send_photo(message.from_user.id,
                                 i[2],
                                 caption=f"Pfoto: {i[3]}\n"
                                         f"Name dish: {i[4]}\n"
                                         f"Description: {i[5]}\n"
                                         f"Price: {i[6]}\n\n"
                                         f"{i[1]}\n",)
    else:
        await message.answer("You are not admin!!!")


def register_hendler_fsmanketa(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands="cancel")
    dp.register_message_handler(cancel_registration,
                                Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['register'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(load_name_dish, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.surname)
    dp.register_message_handler(load_price, state=FSMAdmin.age)