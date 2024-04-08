from env.Role import RoleWithTask, validate_syntax, validate_json, get_json


class Maker(RoleWithTask):
    def __init__(self, *args, **kwargs):
        self.recode = False
        super().__init__(*args, **kwargs)

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
        if not(text.find('pass') == -1):
            return False
        return validate_syntax(text)

    example_text = ('from PIL import Image, ImageDraw\n'
                    'import io\n'
                    'from typing import BinaryIO\n'
                    'def create_photo_PNG()-> BinaryIO:\n'
                    '\t\\"\\"\\" create photo\\"\\"\\"\n'
                    '\timage = Image.new("RGB", (width, height), (255, 255, 255))\n'
                    '\timage_bytes_io = io.BytesIO()\n'
                    '\timage.save(image_bytes_io, format="PNG")\n'
                    '\treturn image_bytes_io\n'
                    )

    def example(self) -> str | list[str] | None:
        if self.recode:
            return Maker.example_text
        return ['{"libraries": [pil, typing, io], "function": "'
                ''+Maker.example_text+'"}',
                '{"libraries": [pil, typing, io], "function": "'
                '' + Maker.example_text + '"}',
                '{"libraries": [soundfile, typing, io], "function": "'
                'import soundfile as sf\n'
                'import io\n'
                'from typing import BinaryIO\n'
                'def create_audio_wav() -> BinaryIO:\n'
                '\t\\"\\"\\" create audio\\"\\"\\"\n'
                '\ttime = range(int(44100 * 5))\n'
                '\tsignal = [0.5 * i for i in time]\n'
                '\taudio_bytes_io = io.BytesIO()\n'
                '\tsf.write(audio_bytes_io, signal, sample_rate, format="wav")\n'
                '\treturn audio_bytes_io\n'
                '"}']

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
        return ("Тобі надається функція з документацією і анотацією, але без самої функції."
                "Потрібно створити функцію. "
                " Уяви себе програмістом і виконай усі умови:"
                "\n- Створи тіло для функції. Повертаючий об'єкт повинен мати тип, що прописаний у анотації. Повертаючий "
                "об'єкт також не повинен бути пустим."
                "\n- Якщо повертаючий об'єкт є файлом, у функції в кінці назви має добавитись _ і формат "
                "файлу, наприклад якщо повертаючим об'єктом є BinaryIO, а його дані є фотографією з форматом PNG, в "
                "кінці назви функції має добавитись _PNG."
                "\n- Якщо завдання у описі можна реалізувати за допомогою OpenAI API, тоді використовувати"
                "OpenAI API."
                "\n- Можна використовувати будь які бібліотеки Python."
                "\n- У відповідь записати json, який містить один об'єкт, у якого 2 поля: libraries i function."
                "\n- Якщо функція не використовує жодну бібліотеку, поле libraries повинно мати порожній список."
                "\n- Якщо функція використовує бібліотеку або бібліотеки, поле libraries повинно мати список,"
                "який містить усі використані бібліотеки. Вказувати лише назви біблотек, без шляху, тобто наприклад"
                " якщо у коді використовується scipy.io.wavfile, то у список вписати лише scipy"
                "\n- Поле function повиннен мати код функції разом усіма імпортованими бібліотеками."
                "\n- У тексті функцій перед усіма \" мають стояти \\."
                "\n- У відповіді немає нічого бути крім json."
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
