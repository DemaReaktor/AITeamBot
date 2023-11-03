import OpenAIAPI
from validation import validate_text, validate_int
import inspect
import abc
import ast


def validate_syntax(text: str) -> bool:
    """check text is a Python code
    ignore ```"""
    validate_text(text)
    try:
        ast.parse(text.replace('```', ''))
        return True
    except SyntaxError:
        return False


class Role(abc.ABC):
    """send requests to ChatGPT using a system description"""

    def validate_answer(self, text: str) -> bool:
        """check ChatGPT answer is right as role need to answer"""
        return True

    def assistant(self) -> str | None:
        """an answer of ChatGpt which should be similar"""
        return None

    @abc.abstractmethod
    def system(self) -> str:
        """a description of how ChatGPT should answer the question"""
        pass

    @abc.abstractmethod
    def _change_text(self, text: str) -> str:
        """change text before it will be used for ChatGPT`s request"""
        pass

    def send_request(self, text: str) -> str | None:
        """send a request to the ChatGPT
        :param text is a question which you want to set to the ChatGPT
        :return an answer of the request if answer was validated otherwise None"""
        validate_text(text)
        attention = ' Май на увазі, твоя відповідь має відповідати вказаному формату!!!'
        result = OpenAIAPI.send_request(self.system() + attention, self._change_text(text), self.assistant())
        return result if self.validate_answer(result) else None


class RoleWithTask(Role, abc.ABC):
    """Role which save id of task"""
    def __init__(self, task_id: int):
        validate_int(task_id)
        self.__id = task_id

    @property
    def task_id(self):
        """id of task role are created for"""
        return self.__id
