from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from TelegramBot import bot

dispatcher = Dispatcher()


@dispatcher.message()
async def echo_handler(message: Message) -> None:
    try:
        name = message.text.split("def ", 1)[1].split("(", 1)[0]
    except():
        await bot.send_message(message.chat.id, "this is not function")
        return
    import Functions
    if hasattr(Functions, name):
        await bot.send_message(message.chat.id, "function with this name already exists")
        return
    function = {}
    exec(message.text, globals(), function)
    setattr(Functions, name, function[name])
    file = open("env/Functions.py", "a")
    file.write(message.text+"\n\n")
    await bot.send_message(message.chat.id, str(getattr(Functions, name)()))
