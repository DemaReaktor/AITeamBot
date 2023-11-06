from env.Role import RoleWithTask, validate_json, get_json
from typing import Any
import env.Functions as Functions


class Realizer(RoleWithTask):
    def __init__(self, *args, **kwargs):
        super().__init__(model="gpt-3.5-turbo-16k", *args, **kwargs)

    def validate_answer(self, text: str) -> bool:
        data = validate_json(text)
        if data is None or not isinstance(data, dict):
            return False
        # if no properties
        if not ('name' in data) or not ('args' in data) or not isinstance(data['name'], str):
            return False
        if isinstance(data['args'], str) and data['args'] == 'пусто':
            return True
        return isinstance(data['args'], dict) and (not('file' in data['args']) or data['args']['file'] == 'file_data')

    def example(self) -> str | list[str] | None:
        return ['{"name":"add", "args": {"a":"3","b":"6","c":"8"}}',
                '{"name":"fibonachi", "args": {"value":"8"}}',
                '{"name":"change_image", "args": {"file":"file_data"}}',
                '{"name":"text_to_speech", "args": {"file":"file_data","language":"ua"}}',
                '{"name":"get_time", "args": "пусто"}']

    def system(self) -> str:
        return ("Тобі надається текст, його зміст:"
                "'завдання:\"<текст>\",\n функції:\"<файл>\"'. Текст замість <файл> містить Python"
                "функції, а замість <текст>  - завдання. Треба знайти функцію, яка розв'яже це завдання,"
                " якщо дані із завдання внести в параметри функції. Виберай лише з тих функцій, які повертають результат"
                "типу str або BinaryIO"
                " Виконай усі умови:"
                "\n1. Вибери лише ті функції, які повертають результат лише типу str або BinaryIO."
                "\n2. Визнач яка функція найкраще підійде для розв'язання цього завдання."
                "\n3. Функція має параметри. Визнач, які дані треба ввести у ці параметри, дані можна брати із завдання."
                "Якщо є параметр file з типом BinaryIO, у цей параметр не треба нічого визначати."
                "\n4. у відповідь записати json, який містить лише один об'єкт, який містить 2 поля: name i args."
                "\n5. Поле name повинно містити назву функції, яку визначив у 1 пункті."
                "\n6. Якщо функція не має параметрів, поле args повинно мати значення 'пусто'"
                "\n7. Якщо функція має параметри, поле args повинно містити об'єкт. Цей об'єкт повиннен містити поля,"
                " назва кожного поля є назва"
                " відповідного параметру, значення кожного поля є дані, які ти визначив у 2 пункті. "
                "\n8. Кількість полей в об'єкті має дорівнювати кількості параметрів функції."
                "\n9. У відповіді немає нічого бути крім json."
                "\n Усі умови повинні виконуватись. Наголошую, відповідь повинна містити лише json!!! ")

    def _change_text(self, text: str) -> str:
        file_text = open(Functions.__file__, "rb").readlines()
        return f"завдання:\"{text}\",\n функції:\"{file_text}\""

    @property
    def kwargs(self) -> dict[str, Any] | None:
        """get a dictionary of parameters which are used with function
        :return a dictionary of parameters. If args are not needed return None"""
        if not hasattr(self, '_Realizer__kwargs'):
            return None
        return self.__kwargs

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if result is None:
            return None
        # get name and args
        data = get_json(result)
        # get args
        if data['args'] == "пусто":
            self.__kwargs = None
        else:
            self.__kwargs = data['args']
        # return name
        return data['name']