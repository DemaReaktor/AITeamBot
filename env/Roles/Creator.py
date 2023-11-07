from env.Role import RoleWithTask, validate_json, validate_bool, get_json


class Creator(RoleWithTask):
    def __init__(self, *args, **kwargs):
        self.__input = False
        self.__output = False
        super().__init__(model="gpt-3.5-turbo-16k", *args, **kwargs)

    def validate_answer(self, text: str) -> bool:
        # validate json
        data = validate_json(text)
        if data is None or not isinstance(data, dict):
            return False
        if ('name' in data) and ('description' in data) and ('input' in data) and ('output' in data):
            return validate_bool(data['input']) and validate_bool(data['output'])
        return False

    def example(self) -> str | list[str] | None:
        return ['{"name": "add", "description": "adds elements", "input":"ні", "output":"ні"}',
                '{"name": "minus", "description": "minus elements", "input":"ні", "output":"ні"}',
                '{"name": "multiply", "description": "multiplies elements", "input":"ні", "output":"ні"}',
                '{"name":"random int","description":"return random int", "input":"ні", "output":"ні"}',
                '{"name":"range","description":"set int into range", "input":"ні", "output":"ні"}',
            '{"name":"photo_to_binaryio", "description":"convert object of type Image into object of type BinaryIO"'
            ', "input":"так", "output":"так"}']

    def system(self) -> str:
        # checker should return a list which has elements as name of step and his description
        return ("Тобі надається текст завдання. Треба описати завдання."
                " Виконай усі умови:"
                "\n1. Створи опис завдання."
                "\n2. У відповідь записати лише json текст, який містить об'єкт."
                "\n3. Об'єкт повиннен мати 4 поля: name, description, input i output."
                "\n4. Придумати для завдання загальну назву. Поле name повинно мати цю назву."
                "\n5. Поле description повинно мати опис завдання."
                "\n6. Поле input повинно мати значення 'так' або 'ні'. Якщо завдання вимагає отримання якогось файлу"
                "(фотографії, документу, аудіо, відео та інші файли),"
                "значення повинно бути 'так', якщо ж завдання не виагає ніякого файлу(фотографії, документу, аудіо,"
                "відео та інші файли), тоді значення має бути 'ні'."
                "\n7. Поле output повинно мати значення 'так' або 'ні'. Якщо завдання вимагає повернення якогось файлу,"
                "значення повинно бути 'так', якщо ж завдання не має повертати ніякого файлу(фотографії, документу,"
                " аудіо, відео та інші файли), тоді значення має бути 'ні'."
                "\n8. У відповіді немає нічого бути крім json тексту."
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
    def input(self) -> bool:
        """get a list of libraries which are used in code of the last request
        :return a list of libraries. If libraries are not needed return None"""
        return self.__input

    @property
    def output(self) -> bool:
        """get a list of libraries which are used in code of the last request
        :return a list of libraries. If libraries are not needed return None"""
        return self.__output

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if not isinstance(result, str):
            return result
        data = get_json(result)
        self.__input = data['input'] == 'так'
        self.__output = data['output'] == 'так'
        self.__name = data['name']
        self.__description = data['description']
        return result

