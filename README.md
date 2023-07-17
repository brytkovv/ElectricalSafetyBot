🤖 <b>ElectricalSafetyBot</b> ⚡️ - бот для прохождения тестов по электробезопасности.
-------------
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Electrosafety_bot) <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=&size=28&pause=1000&color=2662D4&center=true&vCenter=true&width=105&height=30&lines=%3C-+%D0%91%D0%9E%D0%A2" alt="Typing SVG" /></a>

Данный бот построен на <b>aiogram3</b>, <b>postgreSQL</b>, <b>redis</b>, шаблонах <b>jinja</b>, сформирован <b>docker-compose.yaml</b>
Построен на шаблоне <b>https://github.com/MassonNN/masson-aiogram-template</b> 
                
----
Для установки:
1. Клонируйте этот репозиторий  `git clone ...`
2. Создайте файл .env (это полное название файла, включая расширение) с переменными окружения в корневой папке, с содержимым такого вида:

```
POSTGRES_DB=db
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
POSTGRES_HOST=db

REDIS_HOST=redis
REDIS_PASSWORD=redis

BOT_TOKEN = '123456789:ASD_VjnhasdVJJ' # здесь укажите свой токен
DEBUG=0

LOGGING_LEVEL=1

TG_BOT_ADMIN = "123, 456, 789"
```

3.  Перейдите в папку содержащую <b>docker-compose.yaml</b> и введите в консоль `docker-compose up -d --build` (при условии что у вас установлен <b>docker</b> и <b>docker-compose</b>).
Либо замените <b>POSTGRES_HOST</b> и <b>REDIS_HOST</b> на <b>localhost</b> и запускайте без контейнеризации (необходимо иметь устанвленные <b>redis</b> и <b>postgreSQL</b>, а так же все пакеты, используемые в проекте. Для установки `pip install -r requiements.txt`)

                
----

<b>Функции бота</b>

🧩 В настройках вы можете выбрать количество вопросов, тему и отображение оповещений при правильном ответе.
🎲 По умолчанию выбрана <b>IV группа</b>, <b>10 вопросов</b> и включены оповещения.

⏳ Время на ответ не ограничено.
🏆 Тест считается успешным при <b>80%</b> правильных ответов.

🎯 Если вы ошиблись- всплывает правильный ответ.

🔧 Если у вас есть свои предложения по модернизации, если вы нашли ошибки, если у вас есть свои варианты теста в текстовом виде, пишите мне
             