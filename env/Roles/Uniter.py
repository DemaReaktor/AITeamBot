
from env.Role import RoleWithTask, validate_syntax
import env.Functions as Functions


class Uniter(RoleWithTask):
    def validate_answer(self, text: str) -> bool:
        return validate_syntax(text)

    def assistant(self) -> str | None:
        return '<код Python>'

    def system(self) -> str:
        # uniter gets old function in Function.py file and new functions
        # he returns a text which has all functions
        return ("Тобі надається текст, який містить функції (будем їх називати основні),"
                " потім коментар '#------------------',"
                " потім ще функції (будем їх називати допоміжні).Усі функції мови Python. "
                "Треба поєднати два текста в один і створити загальний текст функцій Python. "
                "Однакові функції вписати лише один раз. "
                "У відповідь вписати лише один поєднаний текст.")

    def _change_text(self, text: str) -> str:
        file_text = open(Functions.__file__, "rb").readlines()
        # get all names of functions
        names = [element.split('(')[0] for element in str(file_text).split('def ')]
        for element in names:
            # rewrite all names that exist in Functions.py file and new functions at the same time
            # There It adds _ at the end of name of new function
            text = text.replace(element, element+'_')
        # return new functions and old functions in Function.py file
        return text + '\r\n#------------------\r\n' + str(file_text)

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if result is None:
            return None
        # remove ``` of text
        return result.replace('```', '')
