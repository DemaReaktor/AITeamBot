from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from TelegramBot import bot
from Roles.Roles import role

dispatcher = Dispatcher()


@dispatcher.message()
async def echo_handler(message: Message) -> None:
    if message.content_type == ContentType.TEXT:
        # checker
        new_message = await bot.send_message(message.chat.id, "Завантаження менеджера")
        text = role("checker").send_request(message.text)
        await bot.edit_message_text(text, message.chat.id, new_message.message_id)
        # creator
        new_message = await bot.send_message(message.chat.id, "Завантаження творця")
        text = role("creator").send_request(message.text)
        await bot.edit_message_text(text, message.chat.id, new_message.message_id)
        # maker
        if not(text == "None"):
            new_message = await bot.send_message(message.chat.id, "Завантаження розробника")
            text = role("maker").send_request(text)
            await bot.edit_message_text(text, message.chat.id, new_message.message_id)
    # try:
    #     name = message.text.split("def ", 1)[1].split("(", 1)[0]
    # except():
    #     await bot.send_message(message.chat.id, "this is not function")
    #     return
    # import Functions
    # if hasattr(Functions, name):
    #     await bot.send_message(message.chat.id, "function with this name already exists")
    #     return
    # function = {}
    # exec(message.text, globals(), function)
    # setattr(Functions, name, function[name])
    # file = open("env/Functions.py", "a")
    # file.write(message.text+"\n\n")
    # await bot.send_message(message.chat.id, str(getattr(Functions, name)()))
