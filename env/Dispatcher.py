from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from TelegramBot import bot
from Roles.Tester import Tester
from Roles.Checker import Checker
from Roles.Creator import Creator
from Roles.Maker import Maker
from Roles.Realizer import Realizer
from Roles.Uniter import Uniter

dispatcher = Dispatcher()


async def send_message(role, text, chat_id, role_loading):
    new_message = await bot.send_message(chat_id, role_loading)
    text = role.send_request(text)
    await bot.edit_message_text(text, chat_id, new_message.message_id)
    return text


@dispatcher.message()
async def echo_handler(message: Message) -> None:
    if message.content_type == ContentType.TEXT:
        checker = Checker()
        creator = Creator()
        uniter = Uniter()
        realizer = Realizer()
        text = message.text
        while True:
            # checker
            answer = await send_message(checker, text, message.chat.id, "Завантаження менеджера")
            if answer == 'yes':
                break
            # creator
            text = await send_message(creator, text, message.chat.id, "Завантаження творця")
            # maker
            maker = Maker()
            tester = Tester()
            text = await send_message(maker, text, message.chat.id, "Завантаження розробника")
            # maker can recode functions
            maker.recode = True
            # tester
            while True:
                await send_message(tester, text, message.chat.id, "Завантаження тестера")
                if tester.test_falls is None:
                    break
                # maker with recode
                text = await send_message(maker, tester.test_falls +
                                          '\r\n#-----------------\r\n' + text,
                                          message.chat.id, "Завантаження розробника")
            # uniter
            text = await send_message(uniter, text, message.chat.id,
                               "Завантаження головного розробника")
        file = open("env/Functions.py", "w")
        file.write(text)
        # realizer
        await send_message(realizer, message.text, message.chat.id, "Завантаження виконувача")
