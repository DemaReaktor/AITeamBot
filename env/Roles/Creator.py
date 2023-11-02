from env.Role import RoleWithTask


class Creator(RoleWithTask):
    def system(self) -> str:
        # checker should return a list which has elements as name of step and his description
        # {name: add ,description: adds numbers},{name: minus ,description: minus numbers},
        return ("Тобі надається текст, його зміст:"
                  " 'завдання:\"<текст>\",\n функції:\"<файл>\"'. Текст замість <файл> містить Python"
                  "функції, а замість <текст>  - завдання. Уяви себе програмістом. Треба розбити завдання "
                "на прості кроки, викреслити з них ті, які можуть бути виконані за допомогою наданих "
                "Python функцій. У відповідь написати список із назв кроків та їх опису (лише "
                "тих кроків, які лишились). Назва і опис мають бути узагальнені та без прив'язок до даних."
                 "Формат кожного кроку: "
                 "'{name:\"<назва>\",'description:\"<опис>\"}', замість <назва> має бути назва кроку,"
                 "замість <опис> має бути опис. Кожен наступний крок має відділятись від попереднього комою."
                " Назви і опис може бути тільки англійською мовою.")

    def _change_text(self, text: str) -> str:
        file_text = open("env/Functions.py", "rb").readlines()
        # input data of request is a text of task and functions which already exist
        return f"завдання:\"{text}\",\n функції:\"{file_text}\""
