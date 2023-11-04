from env.Role import RoleWithTask, validate_json


class Creator(RoleWithTask):
    def __init__(self, task_id: int):
        super().__init__(task_id, "gpt-3.5-turbo-16k")

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

    def assistant(self) -> str | None:
        return ('[{name: <name>, description: <description>}, {name: <name>, description: <description>},'
                '{name: <name>, description: <description>}, {name: <name>, description: <description>}]')

    def system(self) -> str:
        # checker should return a list which has elements as name of step and his description
        # {name: add ,description: adds numbers},{name: minus ,description: minus numbers},
        return ("Тобі надаються текст завдання . Треба розбити завдання "
                "на прості кроки. У відповідь написати json текст, який містить список об'єктів. Кожен об'єкт містить "
                "поле name, значення якого має бути назва кроку, також кожен об'єкт повинен мати поле description, "
                "значення якого має бути опис кроку."
                " Назви і опис може бути тільки англійською мовою.")
