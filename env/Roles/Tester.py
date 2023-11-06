from env.Role import RoleWithTask, validate_syntax, validate_json, get_json


class Tester(RoleWithTask):
    def __init__(self, *args, **kwargs):
        super().__init__(model="gpt-3.5-turbo-16k", *args, **kwargs)

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

    def example(self) -> str | list[str] | None:
        return [('{"tests":"def test_add(self):\n'
                    '\tself.assertEqual(add(1.0, 2.0, 3.0), 6.0)\n'
                    '\tself.assertEqual(add(0.0, 0.0, 0.0), 0.0)\n'
                    '\tself.assertEqual(add(-1.0, -2.0, -3.0), -6.0)\n\n'
                    'def test_minus(self):\n'
                    '\tself.assertEqual(minus(5.0, 3.0, 1.0), 1.0)\n'
                    '\tself.assertEqual(minus(10.0, 2.0, 3.0), 5.0)\n'
                    '\tself.assertEqual(minus(0.0, 0.0, 0.0), 0.0)\n'
                    '\tself.assertEqual(minus(-1.0, -2.0, -3.0), 4.0)", "result":"чисто"}'),
                ('{"tests":"def test_multiply(self):\n'
                 '\tself.assertEqual(multiply(1.0, 2.0, 3.0), 6.0)\n", "result":"def test_multiply(self):\n'
                 '\tself.assertEqual(multiply(1.0, 2.0, 3.0), 6.0)\n"}')
                ]

    def system(self) -> str:
        # tester get all functions
        # he returns all written tests
        # he also returns all tests that fall during running
        # if no one test fall he returns 'чисто'
        return ("Тобі надаються функції мови Python. Уяви себе тестером. Створи unit-тести "
                "для кожної функції. Потім запусти їх."
                " Виконай усі умови:"
                "\n1. У відповідь записати лише json текст, який містить лише один об'єкт, який містить два поля:"
                " tests i result."
                "\n2. Поле tests повинно мати код тестів."
                "\n3. Запусти усі тести, визнач, які тести були неуспішними."
                "\n4. Якщо є хоча б один неуспішний тест, поле result повинно мати код усіх неуспішних тестів."
                "\n5. Якщо ж немає неуспішних тестів, у поле result вписати лише слово 'чисто'."
                "\n6. У відповіді немає нічого бути крім json."
                "\n7. У тексті функцій перед усіма \" мають стояти \\."
                "\n Усі умови повинні виконуватись. Наголошую, у відповіді має бути лише json!!!")

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if result is None:
            return None
        # get tests and fall tests
        data = get_json(result)
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
        if not hasattr(self, '_Tester__test_falls'):
            return None
        return self.__test_falls
