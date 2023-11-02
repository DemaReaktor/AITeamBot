import OpenAIAPI
from validation import validate_text, validate_int
import abc


class Role(abc.ABC):
    """send requests to ChatGPT using a system description"""
    @abc.abstractmethod
    def system(self) -> str:
        """a description of how ChatGPT should answer the question"""
        pass

    @abc.abstractmethod
    def _change_text(self, text: str) -> str:
        """change text before it will be used for ChatGPT`s request"""
        pass

    def send_request(self, text: str) -> str:
        """send a request to the ChatGPT
        :param text is a question which you want to set to the ChatGPT
        :return an answer of the request"""
        validate_text(text)
        return OpenAIAPI.send_request(self.system(), self._change_text(text))


class RoleWithTask(Role, abc.ABC):
    def __init__(self, task_id: int):
        validate_int(task_id)
        self.__id = task_id

    @property
    def task_id(self):
        return self.__id
