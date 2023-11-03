# AI Team Bot
Telegram bot who solves all simple tasks.
He uses ChatGPT.

Телеграм бот, що розв'язує будь-які прості завдання.
Використовує ChatGPT.

# Context

[Bot](#Bot)

[Group to track progress](#Group-to-track-progress)

[Team](#Team)

[Code](#Code)

[Бот](#Бот)

[Група для відстеження прогресу](#Група-для-відстеження-прогресу)

[Команда](#Команда)

[Код](#Код)

# Bot

[Link](https://t.me/AITeamMonologbot)

*Bot name: AITeamBot
*nickname: @AITeamMonologbot.
*commands: help, change_language.

Help: Describes how you can use the bot, namely: write any simple task. The bot will execute it with a delay. Also tells about the /change_language command. At the end, I will tell you about the @teamaiupgrade group.

Change Language: changes the language from Ukrainian to English and vice versa.

If you just write a message, the bot will perceive it as a task that needs to be done. If the message is not text, it will ignore it.

[Back](#Context)

# Group-to-track-progress

Link: [https://t.me/+erndqXxg-vZkMDNi](https://t.me/+erndqXxg-vZkMDNi).

This is a special group where you can see how the bot creates roles that communicate with each other. Each role displays its role and its text in the message.

[Back](#Context)

# Team

Roles: Checker, Creator, Maker, Realizer, Uniter, Tester

Everyone plays an important role

Validator: checks whether the already generated code is sufficient to solve the task.

Creator: divides tasks into steps and names them, describing them in parallel.

Developer: Creates features based on creator names and descriptions. Also edits code after testing based on failed tests.

Tester: creates tests, tests functions.

Lead Developer: Adds new features to existing features.

Executor: based on functions, performs the tasks assigned to the team.

[Back](#Context)

# Code

The main function (main.py) starts the dispatcher (Dispatcher.py) based on the bot (TelegramBot.py).

The bot contains data about the language of each group (or person), and can change it as needed.

The manager contains all the commands and also the function of responding to messages.
When writing a message, the response function creates roles that pass data to each other and output the result at the end. The result is translated according to the language of the group (or person) (Translater.py).

More about role relationships:
1. The validator checks whether a new code needs to be created. If so, go to step 2.
If not, proceed to step 6.
2. The creator creates names and descriptions of new functions. Then step 3.
3. Developer makes functions based on names and description. Then step 4.
4. The tester tests the functions, if not all tests were successful, go to step 3 (only the developer will edit the code based on the tests).
If all the tests were successful, we go to step 5.
5. The main developer adds new functions to the existing ones. Then step 1.
6. The executor solves the task based on the available functions.

Each role is a separate class (All these classes are in their respective files in the Roles folder), but each role is a child of the abstract class Role(Role.py), which has the main functions. A role is implemented by sending requests to the GPT chat, each role has its own (System) request. Requests are created in OpenAIAPI.py.

There is also a Config.py file where the keys, id and other confidential information are located, so this file is not on git, it must be created and your own keys registered.

Functions.py stores all functions created by the command.

[Back](#Context)


# Бот

[Посилання](https://t.me/AITeamMonologbot)

*Назва бота: AITeamBot
*нікнейм: @AITeamMonologbot.
*команди: help, change_language.

Help: описує, як можна використовувати бота, а саме: написати будь-яке просте завдання. Бот із затримкою його виконає. Також розказує про команду /change_language. В кінці розказє про групу @teamaiupgrade.

Change Language: змінює мову з української на англійську і навпаки.

Якщо просто написати повідомлення, бот це сприйме як завдання, яке треба виконати. Якщо повідомлення не текст, він його проігнорує.

[Назад](#Context)

# Група-для-відстеження-прогресу

Посилання: [https://t.me/+erndqXxg-vZkMDNi](https://t.me/+erndqXxg-vZkMDNi).

Це спеціальна група, де видно, як бот створює ролі, які спілкуються між собою. Кожна роль виводить у повідомленні свою роль і свій текст.

[Назад](#Context)

# Команда

Ролі: Валідатор(Checker), Творець(Creator), Розробник(Maker), Виконувач(Realizer), Головний розробник(Uniter) Тестер(Tester) 

Кожен виконує важливу роль

Валідатор: перевіряє чи достатньо вже створеного коду щоб розв'язати завдання.

Творець: розбиває завдання на кроки і називає їх, паралельно описуючи.

Розробник: створює функції на основі назв і описів творця. Також редагує код після тестування на основі провальних тестів.

Тестер: створює тести, тестує функції.

Головний розробник: поєднує нові функції до вже наявних.

Виконувач: на основі функцій виконує поставлену команді завдання.

[Назад](#Context)

# Код

Головна функція (main.py) запускає диспатчера (Dispatcher.py) на основі бота (TelegramBot.py).

Бот містить у собі дані про мову кожної групи(або людини), може змінювати її за потреби.

Диспетчер містить усі команди і також функцію реагування на повідомлення.
При написанні повідомлення функція реагування створює ролі, які передають між собою дані, в кінці виводять результат. Результат перекладається відповідно до мови групи(або людини)(Translater.py). 

Детальніше про відносини ролей: 
1. Валідатор перевіряє, чи треба робити новий код. Якщо так, то переходим до кроку 2.
Якщо ж не треба, переходимо до кроку 6.
2. Творець стоврює назви та описи нових функцій. Далі крок 3.
3. Розробник робить функції на основі назв та опису. Далі крок 4.
4. Тестувальник тестує функції, якщо не всі тести успішно пройшли, переходимо до кроку 3(тільки розробник відредагує код на основі тестів).
Якщо всі тести пройшли успішно, йдемо до кроку 5.
5. Головний розробник додає нові функції до вже наявних. Далі крок 1.
6. Виконувач розв'язує завдання на основі наявних функцій.

Кожна роль є особливим класом (Всі ці класи у відповідних файлах у папці Roles), але кожна роль є дочірньою від абстрактного класу Role(Role.py), який має основні функції. Роль реалізується через надсилання запитів до чату GPT, кожна роль має власний (System)запит. Запити створюються у OpenAIAPI.py. 

Також є файл Config.py, де знаходяться ключі, ід та інша конфідеційна інформація, тому цього файлу немає на гіті, його треба створити і прописати власні ключі.

Functions.py зберігає всі створені командою функції.

[Назад](#Context)
