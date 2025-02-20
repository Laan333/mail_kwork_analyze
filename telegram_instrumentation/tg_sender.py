import logging
import os
import time
import json
import threading
import asyncio
import websockets
import telebot
from telebot import types
from queue import Queue
import dotenv
from server_operations.listener import listen
dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot_group = os.getenv('bot_group')
bot_token = os.getenv('bot_token')
bot = telebot.TeleBot(bot_token)

queue = Queue()  # Очередь для передачи данных между потоками


def split_message(text, max_length=4096):
    """Разбивает длинные сообщения на части"""
    if text:
        if len(text) <= max_length:
            return [text]
        lines = text.splitlines()
        parts = []
        current_part = ''
        for line in lines:
            if len(current_part) + len(line) + 1 <= max_length:
                current_part += line + '\n'
            else:
                parts.append(current_part.strip())
                current_part = line + '\n'
        if current_part:
            parts.append(current_part.strip())

        return parts


def send_message(message: list, links: str, ai_answer:str):
    """Отправка сообщений в Telegram"""
    if len(message) == 4:
        project_name, description, min_price, max_price = message

        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Перейти", url=links)
        keyboard.add(button)

        text = (f'<b>✨Название проекта</b>✨: {project_name}\n'
                f'<i>{description}</i>\n'
                f'<b>💸Минимальная цена💸</b>: {min_price} ₽\n'
                f'<b>💰Максимальная цена💰</b>: {max_price} ₽\n'
                f'<b>🤖Ответ от Нейросети🤖</b>: {ai_answer}')

        splited_message = split_message(text)
        try:
            for msg in splited_message:
                time.sleep(0.5)
                bot.send_message(bot_group, msg, reply_markup=keyboard, parse_mode='HTML')
                logger.info(f"Сообщение успешно отправлено в чат {bot_group}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")


def process_queue():
    """Обрабатывает данные из WebSocket в Telegram"""
    while True:
        data = queue.get()  # Ждёт данные
        if isinstance(data, list):
            for i in range(len(data)):
                scraped_message = data[i]['scraped_info']
                link = data[i]['link']
                ai_answer = data[i]['ai_answer']
                send_message(scraped_message, link, ai_answer)
            # send_message([project_name, description, min_price, max_price], project_link)





def start_ws_listener():
    """Запуск WebSocket в отдельном потоке"""
    asyncio.run(listen(queue))


def start_bot():
    """Запуск бота"""
    bot.polling(none_stop=True)


if __name__ == "__main__":
    logger.info('🚀 Запуск программы')

    # Поток для WebSocket
    ws_thread = threading.Thread(target=start_ws_listener, daemon=True)
    ws_thread.start()

    # Поток для обработки сообщений из очереди
    queue_thread = threading.Thread(target=process_queue, daemon=True)
    queue_thread.start()

    # Запускаем бота в основном потоке
    start_bot()
