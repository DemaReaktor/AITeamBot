from env.Role import RoleWithTask, validate_bool
import env.Functions as Functions


class Checker(RoleWithTask):
    def __init__(self, *args, **kwargs):
        super().__init__(model="gpt-3.5-turbo-16k", *args, **kwargs)

    def validate_answer(self, text: str) -> bool:
        return validate_bool(text)

    def example(self) -> str | list[str] | None:
        return ['ні', 'так']

    def system(self) -> str:
        # checker should return yes if all needed functions already exist in file Functions to solve the task
        # otherwise return no
        return ("тобі надається текст, його зміст:"
                "'завдання:\"<текст>\",\n функції:\"<файл>\"'. Текст замість <файл> містить Python"
                "функції, а замість <текст>  - завдання. Уяви себе програмістом, якому треба"
                "створити програму, яка буде розв'язувати подібні завдання."
                " Треба зрозуміти чи можна за допомогою лише цих "
                "Python функцій виконати завдання."
                "Щоб краще розуміти функції, читай їх документацію та коментарі."
                " Якщо це неможливо, то відповідь має містити лише слово 'ні'. Якщо цілком можливо, "
                "відповідь має містити лише слово 'так'")

    def _change_text(self, text: str) -> str:
        file_text = open(Functions.__file__, "rb").readlines()
        # input data of request is a text of task and functions which already exist
        return f"завдання:\"{text}\",\n функції:\"{file_text}\""
