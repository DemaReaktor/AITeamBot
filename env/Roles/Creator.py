from env.Role import Role


class Creator(Role):
    def name(self):
        return "creator"

    def system(self):
        return ("Тобі надається текст, його зміст:"
                  " 'завдання:\"<текст>\",\n функції:\"<файл>\"'. Текст замість <файл> містить Python"
                  "функції, а замість <текст>  - завдання. Уяви себе програмістом. Треба розбити завдання "
                "на елементарні і водночас узагальнені"
                " завдання, викреслити з них ті, які можуть бути виконані за допомогою наданих "
                "Python функцій. У відповідь написати список із назв завдань та їх опису (лише "
                "тих завдань, які лишились). Опис має бути загальний без прив'язки до конкретних даних."
                 "Формат: "
                 "{'name:\"<назва>\",'description:\"<опис>\"'}', замість <назва> має бути назва завдання,"
                 "замість <опис> має бути опис, кожне наступне завдання ставить кому і знову пише формат"
                 "свого зі своїми значеннями. Назви і опис може бути тільки англійською мовою."
                "Назва повинна бути така, щоб функція на мові Python могла мати таку назву. Також"
                "назва не може бути такою ж, як одна з назв наданих у запиті функцій. "
                "Якщо кількість завдань 0, то відповідь має бути 'None'")

    def _change_text(self, text):
        file_text = open("env/Functions.py", "rb").readlines()
        return f"завдання:\"{text}\",\n функції:\"{file_text}\""
