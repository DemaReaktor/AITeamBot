from env.Role import RoleWithTask
import env.Functions as Functions


class Realizer(RoleWithTask):
    def assistant(self) -> str | None:
        return "<відповідь розв'язання>"

    def system(self) -> str:
        return ("Тобі надається текст, його зміст:"
                "'завдання:\"<текст>\",\n функції:\"<файл>\"'. Текст замість <файл> містить Python"
                  "функції, а замість <текст>  - завдання. Треба за допомогою лише цих функцій розв'язати завдання."
                "У відповідь вписати лише відповідь завдання.")

    def _change_text(self, text: str) -> str:
        file_text = open(Functions.__file__, "rb").readlines()
        return f"завдання:\"{text}\",\n функції:\"{file_text}\""
