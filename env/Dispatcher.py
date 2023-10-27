from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from TelegramBot import bot
from TTSConventer import TTSConventer
import pathlib

dispatcher = Dispatcher()


@dispatcher.message()
async def echo_handler(message: Message) -> None:
    if message.content_type == ContentType.AUDIO:
        await bot.download(message.audio, str(message.message_id) + ".mp3")
        bot.send_message(message.chat.id, TTSConventer.convert(open(str(message.message_id) + ".mp3", 'rb')))
        return
    if message.content_type == ContentType.VOICE:
        await bot.download(message.voice, str(message.message_id)+".mp3")
        bot.send_message(message.chat.id, TTSConventer.convert(open(str(message.message_id) + ".mp3", 'rb')))
        return
