from OpenAIAPI import API
from validation import validate_text
import abc


class Role(abc.ABC):
    @abc.abstractmethod
    def system(self) -> str:
        pass

    @abc.abstractmethod
    def _change_text(self, text: str) -> str:
        pass

    def send_request(self, text: str) -> str:
        validate_text(text)
        new_text = self._change_text(text)
        return API.send_request(self.system(), new_text)
