from env.Role import RoleWithTask, validate_syntax, validate_json, get_json


class Tester(RoleWithTask):
    def __init__(self, task_id: int):
        super().__init__(task_id, "gpt-3.5-turbo-16k")

    def validate_answer(self, text: str) -> bool:
        data = validate_json(text)
        if data is None or not isinstance(data, dict):
            return False
        # if no properties
        if not ('tests' in data) or not ('result' in data):
            return False
        if not isinstance(data['tests'], str) or not isinstance(data['result'], str):
            return False
        return validate_syntax(data['tests']) and (data['result'] == 'чисто' or validate_syntax(data['result']))

    def assistant(self) -> str | None:
        return '{"tests":"<код тестів>", "result":"чисто" або "<код неуспішних тестів>"}'

    def system(self):
        # tester get all functions
        # he returns all written tests
        # he also returns all tests that fall during running
        # if no one test fall he returns 'чисто'
        return ("Тобі надаються функції мови Python. Уяви себе тестером. Створи unit-тести "
                "для кожної функції. Потім запусти їх. Виведи усі тести і результат. У відповідь впиши json текст,"
                "який містить один об'єкт. Цей об'єкт містить поле tests, значення якого текст, у якому "
                "має бути написаний код тестів. "
                "Також об'єкт містить поле result, значення якого має бути слово 'чисто' якщо всі тести пройшли"
                " успішно. Якщо хоча б один тест не пройшов успішно, поле result містите текст, у якому має бути"
                " код тестів, які не пройшли успішно.")

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if result is None:
            return None
        # get tests and fall tests
        data = get_json(text)
        # get fall tests
        if data['result'] == 'чисто':
            self.__test_falls = None
        else:
            self.__test_falls = data['result']
        # return all tests
        return data['tests']

    @property
    def test_falls(self) -> str | None:
        """get all tests which fall during running them
        :return fall tests. If falls tests don`t exist return None"""
        if not hasattr(self, '__test_falls'):
            return None
        return self.__test_falls
