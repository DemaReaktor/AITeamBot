from env.Role import RoleWithTask, validate_syntax, validate_json, get_json


class Maker(RoleWithTask):
    def __init__(self, *args, **kwargs):
        self.recode = False
        super().__init__(model="gpt-3.5-turbo-16k", *args, **kwargs)

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
                    '\treturn add(a, -b, -c)\n')

    def example(self) -> str | list[str] | None:
        if self.recode:
            return Maker.example_text
        return ['{"libraries": [], "functions": "'+Maker.example_text+'"}',
                '{"libraries": [json,openai], "functions": "'+Maker.example_text+'\n\n'
                'import json\nimport openai\ndef generate_and_save_text(prompt, max_tokens=50,'
                                    'output_file="generated_text.json"):\ntry:\nopenai.api_key = "API_OPENAI"\n'
                                   '\nresponse = openai.Completion.create(\nengine="text-davinci-002",\nprompt=prompt,'
                                   '\nmax_tokens=max_tokens\n)\n\ngenerated_text = response.choices[0].text\n\n'
                                   'with open(output_file, "w") as file:\njson.dump({"prompt": prompt, '
                                   '"generated_text": generated_text}, file)\n\nreturn generated_text\n\n'
                                   'except Exception as e:\nreturn str(e)\n\n'
                                    'def generate_and_save_text_to_binaryio(generated_text):\n'
                                    '\toutput_binary_io = io.BytesIO()\n'
                                    '\toutput_binary_io.write(generated_text.encode("utf-8"))\n'
                                    '\toutput_binary_io.seek(0)\n'
                                    '\treturn output_binary_io"}']

    def system(self) -> str:
        # if maker rewrite code after tester find bugs
        if self.recode:
            # maker gets own written functions and all fall tests
            # he returns rewritten functions that all tests did not fall
            return("Тобі надається текст, який містить функції , потім коментар '#-----------------',"
                   " потім тести. Ті тести показують, які помилки є у функціях. Уяви себе розробником, який "
                   "виправляє баги, маючи функції і тести, за допомогою яких тестували ті функції. Треба виправити"
                   "код функцій, щоб не було багів, через які спрацьовують тести."
                   " Виконай усі умови:"
                   "\n1. Виправ функції, щоб усі тести проходили."
                   "\n2. Кожна функція повинна використовувати попередньо створену функцію(2га функція використовує "
                   "1шу функцію, а 3тя функція використовує 2гу функцію і так далі)."
                   "\n3. У відповідь записати лише код усіх функцій разом з їхніми імпортованими модулями."
                   "\n4. Документація, коментарі та все інше у функціях має бути написано англійською мовою."
                   "\n5. У відповіді немає нічого бути крім коду функцій та імпортованих модулів."
                   "\n Усі умови повинні виконуватись.")
        # maker has names and descriptions of functions which he should write
        # he returns a list of libraries which will be used by functions.
        # If no one library is needed he will return 'Немає бібліотек'
        # he also returns a list of functions
        return ("Тобі надається json текст, який містить список об'єктів, кожен з яких має поле name i description. "
                " Уяви себе програмістом і виконай усі умови:"
                "\n1. Розроби функції на мові Python, кожна функція має робити те, що вказано у полі description "
                "відповідного об'єкта у списку."
                "\n2. кількість функцій має дорівнювати кількості об'єктів у списку."
                "\n3. Кожна функція повнина мати назву таку ж як поле name відповідного об'єкта"
                "\n4. Кожна функція повинна мати документацію та анотацію."
                "\n5. Якщо завдання у описі об'єкта можна реалізувати за допомогою OpenAI API, тоді використовуати"
                "OpenAI API."
                "\n6. Можна використовувати будь які бібліотеки Python."
                "\n7. Кожна функція повинна використовувати попередньо створену функцію(2га функція використовує "
                "1шу функцію, а 3тя функція використовує 2гу функцію і так далі)."
                "\n8. Останя функція повинна повертати об'єкт типу str або BinaryIO об'єкт в залежності від того,"
                "що вимагається в описі. Якщо опис вказує на повернення файлу, об'єкт, який має повернути функція,"
                "має бути типу BinaryIO, інакше str."
                "\n9. У відповідь записати json текст, який містить один об'єкт, у якого 2 поля: libraries i functions."
                "\n10. Якщо функції не використовують жодну бібліотеку, поле libraries повинно мати порожній список."
                "\n11. Якщо функції використовують бібліотеку або бібліотеки, поле libraries повинно мати список,"
                "який містить усі використані бібліотеки."
                "\n12. Поле functions повиннен мати код функцій разом усіма імпортованими бібліотеками."
                "\n13. Функція останього опису повиннен повертати значення типу str або BinaryIO"
                "\n14. Документація, коментарі та все інше у функціях має бути написано англійською мовою."
                "\n15. У відповіді немає нічого бути крім json текста."
                "\n Усі умови повинні виконуватись.")

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
