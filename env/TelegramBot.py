from aiogram import Bot
from validation import validate_int
import Config


class LanguageBot(Bot):
    """Bot with languages of every chat"""
    def __init__(self, *args, **kwargs):
        self.__is_ukrainian = dict()
        super().__init__(*args, **kwargs)

    def add(self, chat_id: int):
        """add ability to change language to this chat"""
        validate_int(chat_id)
        if not (chat_id in self.__is_ukrainian.keys()):
            self.__is_ukrainian[chat_id] = True

    def __validate_chat_id(self, chat_id: int):
        """check chat_id has type int and is it in dictionary"""
        validate_int(chat_id)
        if not (chat_id in self.__is_ukrainian.keys()):
            raise ValueError("you should first add this chat to bot")

    def change_language(self, chat_id: int):
        """change language of chat from ukrainian to english and vice versa
        :raise ValueError if chat with this id is not added to bot using function add"""
        self.__validate_chat_id(chat_id)
        self.__is_ukrainian[chat_id] = not self.__is_ukrainian[chat_id]

    def is_ukrainian(self, chat_id: int) -> bool:
        """get true if language of this chat is ukrainian
        :raise ValueError if chat with this id is not added to bot using function add"""
        self.__validate_chat_id(chat_id)
        return self.__is_ukrainian[chat_id]

    def has_chat(self, chat_id: int) -> bool:
        return chat_id in self.__is_ukrainian.keys()


bot = LanguageBot(Config.BOT_TOKEN)
