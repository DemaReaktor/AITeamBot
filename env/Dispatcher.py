from aiogram import Dispatcher
from aiogram.types import Message
from TelegramBot import bot

dispatcher = Dispatcher()


@dispatcher.message()
async def echo_handler(message: Message) -> None:
    await bot.send_message(message.chat.id, "Привіт")
