from aiogram import types, Dispatcher

from house_services.handlers.user_information import start_collecting_user_information


dp = Dispatcher.get_current()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await dp.bot.send_message(message.chat.id, 'Давай начинать')
    await start_collecting_user_information(message)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await dp.bot.send_message(msg.from_user.id, msg.text)
