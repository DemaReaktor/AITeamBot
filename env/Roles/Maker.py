from env.Role import RoleWithTask, validate_syntax


class Maker(RoleWithTask):
    def __init__(self, *args, **kwargs):
        self.recode = False
        super().__init__(*args, **kwargs)

    def validate_answer(self, text: str) -> bool:
        if not self.recode:
            # if not libraries
            if not text.find(':'):
                return False
            # remove libraries
            text = text.split(':', 1)[1]
        return validate_syntax(text)

    def assistant(self) -> str | None:
        if self.recode:
            return '<функції>'
        return 'бібліотека1,бібліотека2,бібліотека3...бібліотека(n):<функції>'

    def system(self) -> str:
        # if maker rewrite code after tester find bugs
        if self.recode:
            # maker gets own written functions and all fall tests
            # he returns rewritten functions that all tests did not fall
            return("Тобі надається текст, який містить функції , потім коментар '#-----------------',"
                   " потім тести. Ті тести показують, які помилки є у функціях. Уяви себе розробником, який "
                   "виправляє баги, маючи фуункції і тести, за допомогою яких тестували ті функції. Треба виправити"
                   "код функцій, щоб не було багів, через які спрацьовують тести. У відповідь вписати лише текст з "
                   "оновленими функціями. Документацію не міняти.")
        # maker has names and descriptions of functions which he should write
        # he returns a list of libraries which will be used by functions.
        # If no one library is needed he will return 'Немає бібліотек'
        # he also returns a list of functions
        return ("Тобі надається json текст, який містить список об'єктів, кожен з яких має поле name i description. "
                "Значення name містить назву функції, а значення description - опис функції."
                " Уяви себе програмістом і напиши функції"
                "на мові Python. Кожен елемент містить назву і опис функції, яка має бути написана."
                "Кожна функція повина мати назву як назву у елементі. Функція повина мати документацію,"
                " причому на англійській мові. Для написання функцій можна використовувати "
                "бібліотеки Python, а також OpenAI API. Відповідь потрібно написати за таким форматом: "
                "'<бібліотеки>: <функції>'. Замість <бібліотеки> мають бути написані бібліотеки "
                "через кому, але якщо жодна бібліотека не потрібна, тоді"
                "напиши замість <бібліотеки> 'Немає бібліотек.'"
                " Замість <функції> має бути лише функції(задокоментовані). ")

    def _change_text(self, text: str) -> str:
        return text

    @property
    def libraries(self) -> list[str] | None:
        """get a list of libraries which are used in code of the last request
        :return a list of libraries. If libraries are not needed return None"""
        if not hasattr(self, '__libraries'):
            return None
        return self.__libraries

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if result is None:
            return None
        # get libraries and functions
        results = result.split(':', 1)
        # get libraries
        if results[0] == 'Немає бібліотек':
            self.__libraries = None
        else:
            self.__libraries = results[0].split(',')
        # return functions
        return results[1].replace('```', '')
