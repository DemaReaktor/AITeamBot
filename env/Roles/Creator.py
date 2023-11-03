from env.Role import RoleWithTask
import env.Functions as Functions
import json
import ast


class Creator(RoleWithTask):
    def validate_answer(self, text: str) -> bool:
        # validate json
        try:
            # load json (ast.literal_eval(json.dumps()) need if properties have ' instead ")
            data = json.loads(ast.literal_eval(json.dumps(text)))
            for element in data:
                # if no needed properties
                if not ('name' in element) or not ('description' in element):
                    return False
            return True
        except():
            return False

    def assistant(self) -> str | None:
        return ('[{name: <name>, description: <description>}, {name: <name>, description: <description>},'
                '{name: <name>, description: <description>}, {name: <name>, description: <description>}]')

    def system(self) -> str:
        # checker should return a list which has elements as name of step and his description
        # {name: add ,description: adds numbers},{name: minus ,description: minus numbers},
        return ("Тобі надається текст, його зміст:"
                  " 'завдання:\"<текст>\",\n функції:\"<файл>\"'. Текст замість <файл> містить Python"
                  "функції, а замість <текст>  - завдання. Уяви себе програмістом. Треба розбити завдання "
                "на прості кроки, викреслити з них ті, які можуть бути виконані за допомогою наданих "
                "Python функцій. У відповідь написати json текст, який містить список об'єктів. Кожен об'єкт містить "
                "поле name, значення якого має бути назва кроку, також кожен об'єкт повинен мати поле description, "
                "значення якого має бути опис кроку."
                " Назви і опис може бути тільки англійською мовою.")

    def _change_text(self, text: str) -> str:
        file_text = open(Functions.__file__, "rb").readlines()
        # input data of request is a text of task and functions which already exist
        return f"завдання:\"{text}\",\n функції:\"{file_text}\""
