from env.Role import RoleWithTask, validate_json, validate_bool, get_json


class Creator(RoleWithTask):
    def __init__(self, *args, **kwargs):
        self.__output = False
        self.__text = ""
        super().__init__(*args, **kwargs)

    def validate_answer(self, text: str) -> bool:
        # validate json
        data = validate_json(text)
        if data is None or not isinstance(data, dict):
            return False
        if ('name' in data) and ('description' in data) and ('output' in data):
            return validate_bool(data['output'])
        return False

    def example(self) -> str | list[str] | None:
        return ['{"name": "add", "description": "adds elements", "output":"ні"}',
                '{"name": "minus", "description": "minus elements", "output":"ні"}',
                '{"name": "multiply", "description": "multiplies elements", "output":"ні"}',
                '{"name":"random int","description":"return random int", "output":"ні"}',
                '{"name":"range","description":"set int into range", "output":"ні"}',
            '{"name":"photo_to_binaryio", "description":"convert object of type Image into object of type typing.BinaryIO"'
            ', "output":"так"}']

    def system(self) -> str:
        # checker should return a list which has elements as name of step and his description
        return ("Тобі надається текст завдання. Треба описати завдання."
                " Виконай усі умови:"
                "\n1. Створи детальний опис завдання."
                "\n2. У відповідь записати лише json текст, який містить об'єкт."
                "\n3. Об'єкт повиннен мати 3 поля: name, description і output."
                "\n4. Придумати для завдання загальну назву. Поле name повинно мати цю назву."
                "\n5. Поле description повинно мати детальний опис завдання."
                "\n6. Поле output повинно мати значення 'так' або 'ні'. Якщо завдання вимагає повернення якогось файлу,"
                "значення повинно бути 'так', якщо ж завдання не має повертати ніякого файлу(фотографії, документу,"
                " аудіо, відео та інші файли), тоді значення має бути 'ні'."
                "\n7. У відповіді немає нічого бути крім json тексту."
                "\n Усі умови повинні виконуватись. Наголошую, у відповіді має бути лише json текст!!! ")

    @property
    def task_name(self) -> str | None:
        """get a list of libraries which are used in code of the last request
        :return a list of libraries. If libraries are not needed return None"""
        if not hasattr(self, '_Creator__name'):
            return None
        return self.__name

    @property
    def description(self) -> str | None:
        """get a list of libraries which are used in code of the last request
        :return a list of libraries. If libraries are not needed return None"""
        if not hasattr(self, '_Creator__description'):
            return None
        return self.__description

    @property
    def output(self) -> bool:
        """get a list of libraries which are used in code of the last request
        :return a list of libraries. If libraries are not needed return None"""
        return self.__output

    @property
    def text(self) -> str:
        """get a list of libraries which are used in code of the last request
        :return a list of libraries. If libraries are not needed return None"""
        return self.__text

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if not isinstance(result, str):
            return result
        data = get_json(result)
        self.__output = data['output'] == 'так'
        self.__name = data['name']
        self.__description = data['description']
        self.__text = (f"def {self.__name}():->"
                       f"{'typing.BinaryIO' if self.__output else 'str'}\n"
                       f"\"\"\"\n{self.__description}\"\"\"")
        return result

