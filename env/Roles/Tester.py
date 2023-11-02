from env.Role import RoleWithTask


class Tester(RoleWithTask):
    def system(self):
        # tester get all functions
        # he returns all written tests
        # he also returns all tests that fall during running
        # if no one test fall he returns 'чисто'
        return ("Тобі надаються функції мови Python. Уяви себе тестером. Створи unit-тести "
                "для кожної функції. Потім запусти їх. Відповіть повина бути така:"
                "'<тести>:<результат>', де замість <тести> мають бути всі написані тести. "
                "Замість <результат> має бути слово 'чисто' якщо всі тести пройшли успішно. Якщо"
                "хоча б один тест не пройшов успішно, замість <результат> виведи всі тести,"
                " які не пройшли успішно.")

    def _change_text(self, text: str) -> str:
        return text

    def send_request(self, text: str) -> str:
        result = super().send_request(text)
        # get tests and fall tests
        results = result.rsplit(':', 1)
        if not (len(results) == 2):
            return result
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
