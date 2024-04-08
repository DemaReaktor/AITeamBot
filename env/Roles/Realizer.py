from env.Role import RoleWithTask
import importlib
import env.Functions as Functions


class Realizer(RoleWithTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_answer(self, text: str) -> bool:
        functions = importlib.import_module("Functions")
        importlib.reload(functions)
        return hasattr(functions, text)

    # def example(self) -> str | list[str] | None:
    #     return ["'add'", "'minus'", "'calculate_days_to_NewYear'", "'generate_photo'"]

    def system(self) -> str:
        return ("Тобі надається текст, його зміст:"
                "'завдання:\"<текст>\",\n функції:\"<файл>\"'. Текст замість <файл> містить Python"
                "функції, а замість <текст>  - завдання. Треба знайти функцію, яка розв'яже це завдання. Визнач, яка "
                " функція найкраще підійде для розв'язання цього завдання із наявних. "
                "У відповідь записати лише назву функції."
                "Повторюю, відповідь повинна містити лише назву функції без додаткового тексту. Кількість слів у "
                "відповіді має бути 1(слова через _ важаютьяся як одне слово, наприклад: add_number це одне слово). ")

    def _change_text(self, text: str) -> str:
        file_text = open(Functions.__file__, "rb").readlines()
        return f"завдання:\"{text}\",\n функції:\"{file_text}\""
