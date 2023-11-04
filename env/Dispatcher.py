from aiogram import Dispatcher, F
from aiogram.types import Message, ContentType
from TelegramBot import bot
from Translater import translate as tr
import Config
import Functions

from Role import RoleWithTask
# roles
from Roles.Tester import Tester
from Roles.Checker import Checker
from Roles.Creator import Creator
from Roles.Maker import Maker
from Roles.Realizer import Realizer
from Roles.Uniter import Uniter


dispatcher = Dispatcher()


def __translate(text: str, chat_id: int) -> str:
    """translate text if language of chat is english"""
    if bot.is_ukrainian(chat_id):
        return text
    return tr(text, "ua", "en")


@dispatcher.message(F.text == '/start')
async def start_command(message: Message) -> None:
    """write hello message when user use command /start"""
    bot.add(message.chat.id)
    await bot.send_message(message.chat.id, "Вітаю! Дайте будь-яке просте завдання, я його в в кілка секунд вирішу!"
                                      "(To see English write /change_language)")


@dispatcher.message(F.text == '/help')
async def help_command(message: Message) -> None:
    """write useful information about bot when user use command /help"""
    if not bot.has_chat(message.chat.id):
        await bot.send_message(message.chat.id, "Спочатку напишіть /start")
        return
    await bot.send_message(message.chat.id, __translate("Напішть будь-яке просте завдання. Бот із затримкою його "
                                                  "виконає.\n\n Щоб змінити мову, напишіть команду /change_language."
                                                  "\n\n Також можна подивитись на прогрес бота, для цього треба зайти"
                                                  " в групу @teamaiupgrade", message.chat.id))


@dispatcher.message(F.text == '/change_language')
async def change_language_command(message: Message) -> None:
    """change language of chat when user use command /change_language"""
    if not bot.has_chat(message.chat.id):
        await bot.send_message(message.chat.id, "Спочатку напишіть /start")
        return
    bot.change_language(message.chat.id)
    await bot.send_message(message.chat.id, __translate("Мову змінено", message.chat.id))


# names of roles
role_names = {Checker: 'Валідатор', Creator: 'Творець', Maker: 'Розробник', Realizer: 'Виконувач',
              Tester: 'Тестер', Uniter: 'Головний розробник'}


async def __send_message(role: RoleWithTask, text: str, role_loading: str) -> str:
    """send a message to group (text is role_loading). Then send request to the ChatGPT and get answer.
    In the end change a text of the message to the answer of the request and return the answer"""
    new_message = await bot.send_message(Config.GROUP_ID, role_loading)
    # while answer is not validated
    while True:

        new_text = role.send_request(text)
        if not (new_text is None):
            break
        await bot.send_message(Config.GROUP_ID, f"відповідь не по формату(роль:{role_names[type(role)]},"
                                                f" task id:{role.task_id}")
    await bot.edit_message_text(role_names[type(role)] + f"\n\nTask id:{role.task_id}\n\n"
                                + new_text, Config.GROUP_ID, new_message.message_id)
    return new_text


@dispatcher.message(F.text.regexp(r'(?!\/start$|\/help$|\/change_language$).*'))
# get messages which are not commands
async def solve_task(message: Message) -> None:
    """do new code and write answer of task"""
    if not bot.has_chat(message.chat.id):
        await bot.send_message(message.chat.id, "Спочатку напишіть /start")
        return
    if message.content_type == ContentType.TEXT:
        task_id = message.message_id
        new_message = await bot.send_message(message.chat.id, __translate("Завантаження...", message.chat.id))
        # initialize roles
        checker = Checker(task_id)
        creator = Creator(task_id)
        uniter = Uniter(task_id)
        realizer = Realizer(task_id)

        text = message.text
        # while checker think functions cant solve a task
        while True:
            # checker
            answer = await __send_message(checker, text, "Завантаження валідатора")
            if answer == 'так':
                break

            # creator
            text = await __send_message(creator, text, "Завантаження творця")

            # maker
            maker = Maker(task_id)
            text = await __send_message(maker, text, "Завантаження розробника")
            # maker can recode functions after tester run tests
            maker.recode = True

            # tester
            tester = Tester(task_id)
            # while tester has tests that fall during running
            while True:
                await __send_message(tester, text, "Завантаження тестера")
                if tester.test_falls is None:
                    break

                # maker with recode
                text = await __send_message(maker, tester.test_falls +
                                            "\r\n#-----------------\r\n" + text, "Завантаження розробника")
            # uniter
            text = await __send_message(uniter, text, "Завантаження головного розробника")
            # save all functions
            file = open(Functions.__file__, "w")
            file.write(text)

        # realizer
        text = await __send_message(realizer, message.text, "Завантаження виконувача")
        await bot.edit_message_text(__translate(text, message.chat.id), message.chat.id, new_message.message_id)
