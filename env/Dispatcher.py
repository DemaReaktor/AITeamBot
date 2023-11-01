from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from TelegramBot import bot
from Role import Role
from Roles.Tester import Tester
from Roles.Checker import Checker
from Roles.Creator import Creator
from Roles.Maker import Maker
from Roles.Realizer import Realizer
from Roles.Uniter import Uniter
import Config

dispatcher = Dispatcher()


async def send_message(role: Role, text: str, role_loading: str) -> str:
    new_message = await bot.send_message(Config.GROUP_ID, role_loading)
    text = role.send_request(text)
    await bot.edit_message_text(text, Config.GROUP_ID, new_message.message_id)
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
            answer = await send_message(checker, text, "Завантаження менеджера")
            if answer == 'yes':
                break
            # creator
            text = await send_message(creator, text, "Завантаження творця")
            # maker
            maker = Maker()
            tester = Tester()
            text = await send_message(maker, text, "Завантаження розробника")
            # maker can recode functions
            maker.recode = True
            # tester
            while True:
                await send_message(tester, text, "Завантаження тестера")
                if tester.test_falls is None:
                    break
                # maker with recode
                text = await send_message(maker, tester.test_falls +
                                          '\r\n#-----------------\r\n' + text, "Завантаження розробника")
            # uniter
            text = await send_message(uniter, text, "Завантаження головного розробника")
        file = open("env/Functions.py", "w")
        file.write(text)
        # realizer
        text = await send_message(realizer, message.text, "Завантаження виконувача")
        await bot.send_message(message.chat.id, text)
