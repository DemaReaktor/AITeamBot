from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from TelegramBot import bot
from Translater import translate as tr
import Config

from Role import Role
# roles
from Roles.Tester import Tester
from Roles.Checker import Checker
from Roles.Creator import Creator
from Roles.Maker import Maker
from Roles.Realizer import Realizer
from Roles.Uniter import Uniter


dispatcher = Dispatcher()


def translate(text, chat_id):
    if bot.is_ukrainian(chat_id):
        return text
    return tr(text, "ua", "en")


async def __send_message(role: Role, text: str, role_loading: str) -> str:
    """send a message to group (text is role_loading). Then send request to the ChatGPT and get answer.
    In the end change a text of the message to the answer of the request and return the answer"""
    new_message = await bot.send_message(Config.GROUP_ID, role_loading)
    text = role.send_request(text)
    await bot.edit_message_text(text, Config.GROUP_ID, new_message.message_id)
    return text


@dispatcher.message()
async def echo_handler(message: Message) -> None:
    bot.add(message.chat.id)
    bot.send_message(message.chat.id, "Вітаю! Дайте будь-яке просте завдання, я його в в кілка секунд вирішу!"
                                      "(To see English write /change_language)")


@dispatcher.message()
async def echo_handler(message: Message) -> None:
    if message.content_type == ContentType.TEXT:
        new_message = await bot.send_message(message.chat.id, translate("Завантаження...", message.chat.id))
        # initialize roles
        checker = Checker()
        creator = Creator()
        uniter = Uniter()
        realizer = Realizer()

        text = message.text
        # while checker think functions cant solve a task
        while True:
            # checker
            answer = await __send_message(checker, text, "Завантаження менеджера")
            if answer == 'yes':
                break

            # creator
            text = await __send_message(creator, text, "Завантаження творця")

            # maker
            maker = Maker()
            text = await __send_message(maker, text, "Завантаження розробника")
            # maker can recode functions after tester run tests
            maker.recode = True

            # tester
            tester = Tester()
            # while tester has tests that fall during running
            while True:
                await __send_message(tester, text, "Завантаження тестера")
                if tester.test_falls is None:
                    break

                # maker with recode
                text = await __send_message(maker, ','.join(tester.test_falls) +
                                            "\r\n#-----------------\r\n" + text, "Завантаження розробника")
            # uniter
            text = await __send_message(uniter, text, "Завантаження головного розробника")
        # save all functions
        file = open("env/Functions.py", "w")
        file.write(text)

        # realizer
        text = await __send_message(realizer, message.text, "Завантаження виконувача")
        await bot.edit_message_text(translate(text, message.chat.id), message.chat.id, new_message.message_id)
