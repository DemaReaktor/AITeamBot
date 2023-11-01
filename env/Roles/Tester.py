from env.Role import Role


class Tester(Role):
    def system(self):
        return ("Тобі надаються функції мови Python. Уяви себе тестером. Створи unit-тести "
                "для кожної функції. Потім запусти їх. Відповіть повина бути така:"
                "'<тести>:<результат>', де замість <тести> мають бути всі написані тести. "
                "Замість <результат> має бути слово 'чисто' якщо всі тести пройшли успішно. Якщо"
                "хоча б один тест не пройшов успішно, замість <результат> виведи всі тести,"
                " які не пройшли успішно.")

    def _change_text(self, text):
        return text

    def send_request(self, text):
        result = super().send_request(text)
        results = result.split(':', 1, reverse=True)
        if not (len(results) == 2):
            return result
        if results[1] == 'чисто':
            self.__test_falls = None
        else:
            self.__test_falls = results[1].split(',')
        return result[0]

    @property
    def test_falls(self):
        if not hasattr(self, '__test_falls'):
            return None
        return self.__test_falls
