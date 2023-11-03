from env.Role import RoleWithTask
import env.Functions as Functions


class Checker(RoleWithTask):
    def validate_answer(self, text: str) -> bool:
        return text in ['так', 'ні']

    def assistant(self) -> str | None:
        return 'так або ні'

    def system(self) -> str:
        # checker should return yes if all needed functions already exist in file Functions to solve the task
        # otherwise return no
        return ("тобі надається текст, його зміст:"
                "'завдання:\"<текст>\",\n функції:\"<файл>\"'. Текст замість <файл> містить Python"
                  "функції, а замість <текст>  - завдання. Уяви себе програмістом, якому треба"
                "створити програму, яка буде розв'язувати подібні завдання."
                " Треба зрозуміти чи можна за допомогою лише цих "
                  "Python функцій виконати завдання, без створення нового коду, а лише запустивши відразу "
                "готову функцію. Якщо це неможливо, то відповідь має містити лише слово 'ні'. Інакше"
                "відповідь має містити лише слово 'так'")

    def _change_text(self, text: str) -> str:
        file_text = open(Functions.__file__, "rb").readlines()
        # input data of request is a text of task and functions which already exist
        return f"завдання:\"{text}\",\n функції:\"{file_text}\""
