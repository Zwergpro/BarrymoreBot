from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from house_services.states import UserInformation

dp = Dispatcher.get_current()


@dp.message_handler(commands=['aboutme'])
async def start_collecting_user_information(message: types.Message):
    """Start collecting user information"""
    await UserInformation.fio.set()
    await dp.bot.send_message(message.chat.id, 'Для начала укажи свое ФИО')


@dp.message_handler(state=UserInformation.fio)
async def process_fio(message: types.Message, state: FSMContext):
    """Process user fio"""
    async with state.proxy() as data:
        data['fio'] = message.text

    await UserInformation.address.set()
    await dp.bot.send_message(message.chat.id, 'Теперь укажи свой адрес')


@dp.message_handler(state=UserInformation.address)
async def process_address(message: types.Message, state: FSMContext):
    """Process user address"""
    async with state.proxy() as data:
        data['address'] = message.text

    await dp.bot.send_message(message.chat.id, 'Отлично! Теперь давай проверим всю информацию')
    await UserInformation.confirmation.set()
    await process_confirmation(message, state)


@dp.message_handler(state=UserInformation.confirmation)
async def process_confirmation(message: types.Message, state: FSMContext):
    """Confirm user information"""
    async with state.proxy() as data:
        fio = data['fio']
        address = data['address']

    await dp.bot.send_message(
        message.chat.id,
        'Вот твои данные:\n'
        f'ФИО: {fio}\n'
        f'Адрес: {address}\n',
    )

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='user_info_confirmation_yes'))
    keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='user_info_confirmation_no'))
    await message.answer('Все верно?', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='user_info_confirmation_'), state=UserInformation.confirmation)
async def callbacks_user_info_confirmation(call: types.CallbackQuery, state: FSMContext):
    confirmation_status = call.data.split('_')[-1]
    if confirmation_status == 'yes':
        await state.finish()
        await dp.bot.send_message(call.message.chat.id, 'Супер! Теперь я к твоим услугам')
        await call.answer()
        return

    await dp.bot.send_message(call.message.chat.id, 'Черт! Что-то пошло не так( Давай повторим')
    await call.answer()
    await start_collecting_user_information(call.message)
