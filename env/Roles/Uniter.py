from env.Role import RoleWithTask, validate_syntax
import env.Functions as Functions


class Uniter(RoleWithTask):
    def validate_answer(self, text: str) -> bool:
        return validate_syntax(text)

    def example(self) -> str | list[str] | None:
        return ('def add(a: float, b: float, c: float) -> float:\n'
                    '\t""" adds elements""""\n'
                    '\treturn a + b + c\n'
                    '\n'
                    'def minus(a: float, b: float, c: float) -> float:\n'
                    '\t""" minus elements""""\n'
                    '\treturn a - b - c\n')

    def system(self) -> str:
        # uniter gets old function in Function.py file and new functions
        # he returns a text which has all functions
        return ("Тобі надається текст, який містить функції (будем їх називати основні),"
                " потім коментар '#------------------',"
                " потім ще функції (будем їх називати допоміжні).Усі функції мови Python. "
                "Треба поєднати два текста в один і створити загальний текст функцій Python. Усі використані "
                "бібліотеки залишити на початку тексту. "
                " Виконай усі умови:"
                "\n1. У відповідь записати лише код усіх функцій разом з їхніми імпортованими модулями."
                "\n2. Документація, коментарі та все інше у функціях має бути написано англійською мовою."
                "\n3. Усі модулі мають бути записані(зімпортовані) на початку коду."
                "\n4. Подібні функції(якщо 2 функції мають різні аргументи або повертають об'єкти різних типів,"
                "вони не є подібними, також подібними не є функції, які виконують різні завдання)"
                " не писати двічі, натомість на їх основі написати узагальнену функцію, яка "
                "буде виконувати завдання обох функцій."
                "\n5. У відповіді немає нічого бути крім коду функцій та імпортованих модулів."
                "\n6. У тексті функцій перед усіма \" мають стояти \\."
                "\n Усі умови повинні виконуватись. Наголошую, у відповіді має бути лише json!!! ")

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
        if not isinstance(result, str):
            return result
        # remove ``` of text
        return result.replace('```', '')
