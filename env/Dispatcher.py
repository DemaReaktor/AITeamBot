from aiogram import Dispatcher, F
from openai.error import OpenAIError, RateLimitError, ServiceUnavailableError
from aiogram.types import Message, ContentType, BufferedInputFile
from TelegramBot import bot
import importlib
from Translater import translate as tr
from typing import BinaryIO, Type
import Config
import pip

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


@dispatcher.message(F.text == None)
# get messages with no text
async def empty_message(message: Message) -> None:
    if not bot.has_chat(message.chat.id):
        await bot.send_message(message.chat.id, "Спочатку напишіть /start")
        return
    if not (message.md_text == ''):
        return await solve_task(message)
    await bot.send_message(message.chat.id, __translate("Ви маєте написати завдання", message.chat.id))


async def __send_message(role: RoleWithTask, text: str, role_loading: str) -> str | Type:
    """send a message to group (text is role_loading). Then send request to the ChatGPT and get answer.
    In the end change a text of the message to the answer of the request and return the answer"""
    new_message = await bot.send_message(Config.GROUP_ID, role_loading)
    # while answer is not validated
    while True:
        new_text = role.send_request(text)
        if isinstance(new_text, type):
            await bot.send_message(Config.GROUP_ID, f"помилка:{str(new_text)}")
            return new_text
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
    if message.content_type in [ContentType.TEXT, ContentType.DOCUMENT]:
        chat_id = message.chat.id
        message_text = message.text
        if message_text is None:
            message_text = message.md_text
        task_id = message.message_id
        new_message = await bot.send_message(message.chat.id, "Завантаження...")
        # initialize roles
        checker = Checker(task_id, chat_id)
        creator = Creator(task_id, chat_id)
        uniter = Uniter(task_id, chat_id)
        realizer = Realizer(task_id, chat_id)

        # while checker think functions cant solve a task
        while True:
            # checker
            answer = await __send_message(checker, message_text, "Завантаження валідатора")
            if isinstance(answer, type):
                return await bot.send_message(chat_id, __translate("бот зараз дуже зайнятий, спробуйте через"
                                                                   "5 хв", chat_id))
            if answer == 'так':
                break

            # creator
            text = await __send_message(creator, message_text, "Завантаження творця")
            if isinstance(text, type):
                return await bot.send_message(chat_id, __translate("бот зараз дуже зайнятий, спробуйте через"
                                                                   "5 хв", chat_id))

            # maker
            maker = Maker(task_id, chat_id)
            text = await __send_message(maker, text, "Завантаження розробника")
            if isinstance(text, type):
                return await bot.send_message(chat_id, __translate("бот зараз дуже зайнятий, спробуйте через"
                                                                   "5 хв", chat_id))
            # maker can recode functions after tester run tests
            maker.recode = True

            # tester
            tester = Tester(task_id, chat_id)
            # while tester has tests that fall during running
            while True:
                await __send_message(tester, text, "Завантаження тестера")
                if isinstance(text, type):
                    return await bot.send_message(chat_id, __translate("бот зараз дуже зайнятий, спробуйте через"
                                                                       "5 хв", chat_id))
                if tester.test_falls is None:
                    break

                # maker with recode
                text = await __send_message(maker, tester.test_falls +
                                            "\r\n#-----------------\r\n" + text, "Завантаження розробника")
            # uniter
            text = await __send_message(uniter, text, "Завантаження головного розробника")
            if isinstance(text, type):
                return await bot.send_message(chat_id, __translate("бот зараз дуже зайнятий, спробуйте через"
                                                                   "5 хв", chat_id))
            # save all functions
            if not(maker.libraries is None):
                for library in maker.libraries:
                    pip.main(['install', library])
            import Functions as functions
            with open(functions.__file__, "w", encoding='utf-8') as file:
                file.write(text)

        # get text of file
        file = None
        if not (message.document is None):
            file = await bot.get_file(message.document.file_id)
            result = await bot.download_file(file.file_path)
            file = BufferedInputFile(result, f"{chat_id}_{message.message_id}")

        # realizer
        function_name = await __send_message(realizer, message_text, "Завантаження виконувача")
        if isinstance(function_name, type):
            return await bot.send_message(chat_id, __translate("бот зараз дуже зайнятий, спробуйте через"
                                                               "5 хв", chat_id))
        functions = importlib.import_module("Functions")
        importlib.reload(functions)
        if realizer.kwargs is None:
            text = getattr(functions, function_name)()
        else:
            if 'file' in getattr(functions, function_name).__code__.co_varnames and file is None:
                bot.send_message(__translate("завдання вимає файлу, який не прикріплений до тексту",
                                             message.chat.id), message.chat.id)
                return
            if 'file' in realizer.kwargs:
                data = realizer.kwargs
                data.pop('file')
                text = getattr(functions, function_name)(file, **realizer.kwargs)
            else:
                text = getattr(functions, function_name)(**realizer.kwargs)
        if isinstance(text, BinaryIO):
            await bot.edit_message_text(__translate("Ось тут потрібний "
                                                    "вам файл", chat_id), chat_id, new_message.message_id)
            await bot.send_document(chat_id, text)
        elif isinstance(text, str):
            await bot.edit_message_text(__translate(text, chat_id), chat_id, new_message.message_id)
        else:
            await bot.edit_message_text(__translate(str(text), chat_id), chat_id, new_message.message_id)
