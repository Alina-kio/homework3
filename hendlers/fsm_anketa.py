from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot
from keyboards.client_kb import cancel_markup

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


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


async def loat_photo(message: types.Message, state: FSMAdmin):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Enter name of the dish...")


async def loat_name(message: types.Message, state: FSMAdmin):
    async with state.proxy() as data:
        data['dish name'] = message.text
    await FSMAdmin.next()
    await message.answer("Enter description of the dish...")


async def loat_discription(message: types.Message, state: FSMAdmin):
    async with state.proxy() as data:
        data['discription'] = message.text
    await FSMAdmin.next()
    await message.answer("Enter price...")


async def loat_price(message: types.Message, state: FSMAdmin):
    try:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await state.finish()
        await message.answer('You can be free)')
    except:
        await message.answer('Only number!!!')
    

async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply('Registration canceled!')



def register_hendler_fsmanketa(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands="cancel")
    dp.register_message_handler(cancel_registration, Text(equals='cancel', ignore_case=True), state='*')


    dp.register_message_handler(fsm_start, commands=['register'])
    dp.register_message_handler(loat_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(loat_name, state=FSMAdmin.name)
    dp.register_message_handler(loat_discription, state=FSMAdmin.description)
    dp.register_message_handler(loat_price, state=FSMAdmin.price)