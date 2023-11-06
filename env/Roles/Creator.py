from env.Role import RoleWithTask, validate_json


class Creator(RoleWithTask):
    def __init__(self, *args, **kwargs):
        super().__init__(model="gpt-3.5-turbo-16k", *args, **kwargs)

    def validate_answer(self, text: str) -> bool:
        # validate json
        data = validate_json(text)
        if data is None or not isinstance(data, list):
            return False
        for element in data:
            # if no needed properties
            if not ('name' in element) or not ('description' in element):
                return False
        return True

    def example(self) -> str | list[str] | None:
        return [('[{"name": "add", "description": "adds elements"}, {"name": "minus", "description": "minus elements"},'
                '{"name": "multiply", "description": "multiplies elements"}]'),
                '[{"name":"random int","description":"return random int"},{"name":"range","description":"set int '
                'into range"}]']

    def system(self) -> str:
        # checker should return a list which has elements as name of step and his description
        return ("Тобі надається текст завдання. Треба розбити завдання на прості кроки."
                " Виконай усі умови:"
                "\n1. Створи список послідовних кроків."
                "\n2. У відповідь записати лише json, який містить список."
                "\n3. Кожен об'єкт у списку повиннен мати два поля: name i description."
                "\n4. Поле name повинно мати назву відповідного кроку."
                "\n5. Поле description повинно мати опис відповідного кроку."
                "\n6. Значення полей name i description мають бути написанні англійською мовою."
                "\n7. У відповіді немає нічого бути крім json текста."
                "\n Усі умови повинні виконуватись. Наголошую, у відповіді має бути лише json!!! ")

