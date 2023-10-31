# check, idea, do, test, (check), realise
from OpenAIAPI import API
from validation import validate_text
import abc


class Role(abc.ABC):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def system(self):
        pass

    @abc.abstractmethod
    def _change_text(self, text):
        pass

    def send_request(self, text):
        validate_text(text)
        new_text = self._change_text(text)
        return API.send_request(self.system(), new_text)
