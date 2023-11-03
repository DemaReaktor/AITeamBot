from env.Role import RoleWithTask, validate_syntax


class Tester(RoleWithTask):
    def validate_answer(self, text: str) -> bool:
        # not valid if text doesnt have tests and answer
        if text.find('\n#-1-1-1-1-1-1-1-1\n') == -1:
            return False
        results = text.split('\n#-1-1-1-1-1-1-1-1\n', 1)
        # validate tests and answer
        return validate_syntax(results[0]) and (results[1] == 'чисто' or validate_syntax(results[1]))

    def assistant(self) -> str | None:
        return '<код тестів>\n#-1-1-1-1-1-1-1-1\n(чисто або <код неуспішних тестів>)'

    def system(self):
        # tester get all functions
        # he returns all written tests
        # he also returns all tests that fall during running
        # if no one test fall he returns 'чисто'
        return ("Тобі надаються функції мови Python. Уяви себе тестером. Створи unit-тести "
                "для кожної функції. Потім запусти їх. Виведи усі тести і результат. Відповіть повина бути така:"
                "'<тести>\n#-1-1-1-1-1-1-1-1\n<результат>', де замість <тести> мають бути написаний код тестів. "
                "Замість <результат> має бути слово 'чисто' якщо всі тести пройшли успішно. Якщо "
                "хоча б один тест не пройшов успішно, замість <результат> виведи код тестів,"
                " які не пройшли успішно.")

    def _change_text(self, text: str) -> str:
        return text

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if result is None:
            return None
        # get tests and fall tests
        results = result.rsplit('\n#-1-1-1-1-1-1-1-1\n', 1)
        # get fall tests
        if results[1] == 'чисто':
            self.__test_falls = None
        else:
            self.__test_falls = results[1].split(',')
        # return all tests
        return results[0]

    @property
    def test_falls(self) -> list[str] | None:
        """get all tests which fall during running them
        :return fall tests. If falls tests don`t exist return None"""
        if not hasattr(self, '__test_falls'):
            return None
        return self.__test_falls
