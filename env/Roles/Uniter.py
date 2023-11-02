from env.Role import RoleWithTask


class Uniter(RoleWithTask):
    def system(self) -> str:
        # uniter gets old function in Function.py file and new functions
        # he returns a text which has all functions
        return ("Тобі надається текст, який містить функції (будем їх називати основні),"
                " потім коментар '#------------------',"
                " потім ще функції (будем їх називати допоміжні).Усі функції мови Python."
                " І основні, і допоміжні, можуть використовувати модулі. Треба поєднати два текста в один."
                " Прицьому всі модулі винести на початок тексту."
                "У відповідь вписати лише один поєднаний текст.")

    def _change_text(self, text: str) -> str:
        file_text = open("env/Functions.py", "rb").readlines()
        # get all names of functions
        names = [element.split('(')[0] for element in str(file_text).split('def ')]
        for element in names:
            # rewrite all names that exist in Functions.py file and new functions at the same time
            # There It adds _ at the end of name of new function
            text = text.replace(element, element+'_')
        # return new functions and old functions in Function.py file
        return text + '\r\n#------------------\r\n' + str(file_text)
