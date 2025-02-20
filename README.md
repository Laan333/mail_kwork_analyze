[ENG Version](#Kwork Parser (ENG))
[RUS Версия](#Kwork-Parser-(RU))
## Kwork Parser (RU)
Это не большой парсер kwork.ru. Он собирает с почты рассылочные письма собирает их в нужные ссылки. Отправляет на сервер, все ссылки скрапятся (Название проекта, описание, ценник мин, ценник макс). После пихается в ИИ с последующим анализом (пре промптинг) и отправляется в тг бота.
# Перед запуском обязательно настроить рассылку kwork на почту! (На ваш выбор по таймингам 1час,3часа, 6 часов и раз в день.)
# Запуск сервера uvicorn 
- uvicorn server_operations.server:app --host 0.0.0.0 --port 8000 --reload
# Порядок запуска:
- Запускаем сервер (команда выше)
- Запускаем telegram_instrumentation/tg_sender.py
- Запускаем main.py
- Вуаля
# Не много про .env
- imap_server - указываете imap вашего мыла
- email - указываете сам адрес почты
- password - пароль от вашей почты
- sender - в данном случае news@kwork.ru
- bot_group - группа , куда будет отправляться объявления
- url - локальный адресс вашего ИИ (для ГПТ или some shit нужно редачить).
- bot_token - токен из botfather
# Будущие tasks 20.02.2025
- Если логин не прошел вырубать полностью все процессы❌
- bash.sh с автозапуском всех процессов❌
- Добавить выбор нейросети (добавить api и поддержку платных) ❌
-------------------------------------------------------------------------
## Kwork Parser (ENG)
This is a small parser for kwork.ru. It collects newsletter emails from your inbox and extracts the required links. These links are sent to a server where all the links are scraped to retrieve project data (Project Title, Description, Minimum Price, Maximum Price). After that, the data is sent to an AI for further analysis (pre-prompting) and then forwarded to a Telegram bot.

# Before launching, make sure to set up the Kwork mailing list on your email! (Choose your timing: 1 hour, 3 hours, 6 hours, or once a day.)

# Starting the Server:
Launch the server with uvicorn:
uvicorn server_operations.server:app --host 0.0.0.0 --port 8000 --reload
# Startup Order:
- Start the server (using the command above)
- Start telegram_instrumentation/tg_sender.py
- Start main.py
- Voilà!

# About the .env File
- imap_server: Specify the IMAP server for your email.
- email: Your email address.
- password: The password for your email account.
- sender: In this case, news@kwork.ru.
- bot_group: The Telegram group where announcements will be sent.
- url: The local address of your AI (for GPT or any other service; this might need editing).
- bot_token: The token obtained from BotFather.
# Future Tasks (as of 20.02.2025)
- If the login fails, completely shut down all processes ❌
- Create a bash.sh script for autostarting all processes ❌
- Add an option to choose the AI (integrate an API and support for paid options) ❌
