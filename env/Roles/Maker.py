from env.Role import RoleWithTask, validate_syntax, validate_json, get_json


class Maker(RoleWithTask):
    def __init__(self, task_id: int):
        self.recode = False
        super().__init__(task_id, "gpt-3.5-turbo-16k")

    def validate_answer(self, text: str) -> bool:
        if not self.recode:
            data = validate_json(text)
            if data is None or not isinstance(data, dict):
                return False
            # if no properties
            if not ('libraries' in data) or not ('functions' in data) or not isinstance(data['libraries'], list):
                return False
            if not isinstance(data['functions'], str):
                return False
            for element in data['libraries']:
                if not isinstance(element, str):
                    return False
            text = data['functions']
        return validate_syntax(text.removesuffix('```').removesuffix('python'))

    example_text = ('def add(a: float, b: float, c: float) -> float:\n'
                    '\t""" adds elements""""\n'
                    '\treturn a + b + c\n'
                    '\n'
                    'def minus(a: float, b: float, c: float) -> float:\n'
                    '\t""" minus elements""""\n'
                    '\treturn a - b - c\n')

    def example(self) -> str | list | None:
        if self.recode:
            return Maker.example_text
        return ['{"libraries": [], "functions": "'+Maker.example_text+'"}',
                '{"libraries": [json,openai], "functions": "'+Maker.example_text+'\n\n'
                'def generate_and_save_text(prompt, max_tokens=50,'
                                    'output_file="generated_text.json"):\ntry:\nopenai.api_key = "API_OPENAI"\n'
                                   '\nresponse = openai.Completion.create(\nengine="text-davinci-002",\nprompt=prompt,'
                                   '\nmax_tokens=max_tokens\n)\n\ngenerated_text = response.choices[0].text\n\n'
                                   'with open(output_file, "w") as file:\njson.dump({"prompt": prompt, '
                                   '"generated_text": generated_text}, file)\n\nreturn generated_text\n\n'
                                   'except Exception as e:\nreturn str(e)\n\n"}']

    generate_and_save_text_code = ('output_file="generated_text.json"):\ntry:\nopenai.api_key = "ВАШ_КЛЮЧ_API_OPENAI"\n'
                                   '\nresponse = openai.Completion.create(\nengine="text-davinci-002",\nprompt=prompt,'
                                   '\nmax_tokens=max_tokens\n)\n\ngenerated_text = response.choices[0].text\n\n'
                                   'with open(output_file, "w") as file:\njson.dump({"prompt": prompt, '
                                   '"generated_text": generated_text}, file)\n\nreturn generated_text\n\n'
                                   'except Exception as e:\nreturn str(e)\n\n')

    def system(self) -> str:
        # if maker rewrite code after tester find bugs
        if self.recode:
            # maker gets own written functions and all fall tests
            # he returns rewritten functions that all tests did not fall
            return("Тобі надається текст, який містить функції , потім коментар '#-----------------',"
                   " потім тести. Ті тести показують, які помилки є у функціях. Уяви себе розробником, який "
                   "виправляє баги, маючи фуункції і тести, за допомогою яких тестували ті функції. Треба виправити"
                   "код функцій, щоб не було багів, через які спрацьовують тести. У відповідь вписати лише текст з "
                   "оновленими функціями. Документацію не міняти.")
        # maker has names and descriptions of functions which he should write
        # he returns a list of libraries which will be used by functions.
        # If no one library is needed he will return 'Немає бібліотек'
        # he also returns a list of functions
        return ("Тобі надається json текст, який містить список об'єктів, кожен з яких має поле name i description. "
                "Значення name містить назву функції, а значення description - опис функції."
                " Уяви себе програмістом і напиши функції"
                "на мові Python. Кожен елемент містить назву і опис функції, яка має бути написана."
                "Кожна функція повина мати назву як назву у елементі. Функція повина мати детальну документацію. "
                "Для написання функцій можна використовувати "
                "бібліотеки Python, а також OpenAI API. У відповідь написати json текст, який містить один об'єкт."
                "Об'єкт містить поле libraries, значення якого має бути json список бібліотек, які використовуються("
                "якщо жодні бібліотеки не використовуються, то просто має бути порожній список)."
                "Також об'єкт повинен мати поле functions, "
                "значення якого має бути json текст, що містить лише функцій(задокоментовані).")

    @property
    def libraries(self) -> list[str] | None:
        """get a list of libraries which are used in code of the last request
        :return a list of libraries. If libraries are not needed return None"""
        if not hasattr(self, '__libraries'):
            return None
        return self.__libraries

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if result is None:
            return None
        # get libraries and functions
        data = get_json(result)
        # get libraries
        if len(data['libraries']) == 0:
            self.__libraries = None
        else:
            self.__libraries = data['libraries']
        # return functions
        return data['functions'].replace('```', '').removesuffix('python')
