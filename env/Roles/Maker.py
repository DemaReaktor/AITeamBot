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
            if not ('libraries' in data) or not ('function' in data) or not isinstance(data['libraries'], list):
                return False
            if not isinstance(data['function'], str):
                return False
            for element in data['libraries']:
                if not isinstance(element, str):
                    return False
            text = data['function']
        return validate_syntax(text)

    example_text = ('def add(a: float, b: float, c: float) -> float:\n'
                    '\t\\"\\"\\" adds elements\\"\\"\\"\n'
                    '\treturn a + b + c\n'
                    '\n'
                    'def minus(a: float, b: float, c: float) -> float:\n'
                    '\t\\"\\"\\" minus elements\\"\\"\\"\n'
                    '\treturn add(a, -b, -c)\n')

    def example(self) -> str | list[str] | None:
        if self.recode:
            return Maker.example_text
        return ['{"libraries": [], "function": "'+Maker.example_text+'"}',
                '{"libraries": [json,openai], "function": "'+Maker.example_text+'\n\n'
                'import json\nimport openai\ndef generate_and_save_text(prompt, max_tokens=50,'
                                    'output_file=\\"generated_text.json\\"):\ntry:\nopenai.api_key = \\"API_OPENAI\\"\n'
                                   '\nresponse = openai.Completion.create(\nengine=\\"text-davinci-002\\",\nprompt=prompt,'
                                   '\nmax_tokens=max_tokens\n)\n\ngenerated_text = response.choices[0].text\n\n'
                                   'with open(output_file, \\"w\\") as file:\njson.dump({\\"prompt\\": prompt, '
                                   '\\"generated_text\\": generated_text}, file)\n\nreturn generated_text\n\n'
                                   'except Exception as e:\nreturn str(e)\n\n'
                                    'def generate_and_save_text_to_binaryio(generated_text):\n'
                                    '\toutput_binary_io = io.BytesIO()\n'
                                    '\toutput_binary_io.write(generated_text.encode(\\"utf-8\\"))\n'
                                    '\toutput_binary_io.seek(0)\n'
                                    '\treturn output_binary_io"}']

    def system(self) -> str:
        # if maker rewrite code after tester find bugs
        if self.recode:
            # maker gets own written functions and all fall tests
            # he returns rewritten functions that all tests did not fall
            return("Тобі надається текст, який містить функцію , потім коментар '#-----------------',"
                   " потім тести. Ті тести показують, які помилки є у функції. Уяви себе розробником, який "
                   "виправляє баги, маючи функції і тести, за допомогою яких тестували ті функції. Треба виправити"
                   "код функції, щоб не було багів, через які спрацьовують тести."
                   " Виконай усі умови:"
                   "\n1. Виправ функцію, щоб усі тести проходили."
                   "\n2. У відповідь записати лише код функції разом з їхніми імпортованими модулями."
                   "\n3. Документація, коментарі та все інше у функції має бути написано англійською мовою."
                   "\n4. У відповіді немає нічого бути крім коду функції та імпортованих модулів."
                   "\n5. У тексті функції перед усіма \" мають стояти \\."
                   "\n Усі умови повинні виконуватись.")
        # maker has names and descriptions of functions which he should write
        # he returns a list of libraries which will be used by functions.
        # If no one library is needed he will return 'Немає бібліотек'
        # he also returns a list of functions
        return ("Тобі надається json текст, який містить об'єкт, що має поля name, description, input i output. "
                " Уяви себе програмістом і виконай усі умови:"
                "\n1. Розроби функцію на мові Python, вона має робити те, що вказано у полі description."
                "\n2. Функція повнина мати назву таку ж як поле name."
                "\n3. Функція повинна мати документацію та анотацію."
                "\n4. Якщо завдання у описі можна реалізувати за допомогою OpenAI API, тоді використовуати"
                "OpenAI API."
                "\n5. Можна використовувати будь які бібліотеки Python."
                "\n6. Функція повинна повертати об'єкт типу str якщо значення поля output дорівнює 'ні'."
                "Якщо ж значення поля output є 'так', функція повинна повертати об'єкт типу BinaryIO."
                "\n7. Якщо значення поля input є 'так', функція повинна мати лише один аргумент типу BinaryIO."
                " Якщо ж значення input є 'ні', функції не можна мати аргументів."
                "\n8. Код функції має бути такий, щоб функція виконувала завдання у описі, але прицьому повертала "
                "значення типу, вказаного у пункті 6, і також мала аргументи, вказані у пункті 7."
                "\n9. У відповідь записати json, який містить один об'єкт, у якого 2 поля: libraries i function."
                "\n10. Якщо функція не використовує жодну бібліотеку, поле libraries повинно мати порожній список."
                "\n11. Якщо функція використовує бібліотеку або бібліотеки, поле libraries повинно мати список,"
                "який містить усі використані бібліотеки."
                "\n12. Поле function повиннен мати код функції разом усіма імпортованими бібліотеками."
                "\n13. У тексті функцій перед усіма \" мають стояти \\."
                "\n14. Документація, коментарі та все інше у функції має бути написано англійською мовою."
                "\n15. У відповіді немає нічого бути крім json."
                "\n Усі умови повинні виконуватись. Наголошую, у відповіді має бути лише json!!! ")

    @property
    def libraries(self) -> list[str] | None:
        """get a list of libraries which are used in code of the last request
        :return a list of libraries. If libraries are not needed return None"""
        if not hasattr(self, '_Maker__libraries'):
            return None
        return self.__libraries

    def send_request(self, text: str) -> str | None:
        result = super().send_request(text)
        if not isinstance(result, str):
            return result
        if self.recode:
            return result
        # get libraries and functions
        data = get_json(result)
        # get libraries
        if len(data['libraries']) == 0:
            self.__libraries = None
        else:
            self.__libraries = data['libraries']
        # return functions
        return data['function'].replace('```', '').removesuffix('python')
