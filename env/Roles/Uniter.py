from env.Role import Role


class Uniter(Role):
    def system(self) -> str:
        return ("Тобі надається текст, який містить функції (будем їх називати основні),"
                " потім коментар '#------------------',"
                " потім ще функції (будем їх називати допоміжні).Усі функції мови Python."
                " І основні, і допоміжні, можуть використовувати модулі. Треба поєднати два текста в один."
                " Прицьому всі модулі винести на початок тексту."
                "У відповідь вписати лише один поєднаний текст.")

    def _change_text(self, text: str) -> str:
        file_text = open("env/Functions.py", "rb").readlines()
        names = [element.split('(')[0] for element in str(file_text).split('def ')]
        for element in names:
            text = text.replace(element, element+'_')
        return text + '\r\n#------------------\r\n' + str(file_text)
