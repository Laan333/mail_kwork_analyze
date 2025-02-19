import logging
import os

import telebot
from telebot import types
import threading
from ai_operations.connection_ai import client_data
from ai_operations.lexicon_for_ai import prompt
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


bot_group = os.getenv('bot_group')


bot_token = os.getenv('bot_token')
bot = telebot.TeleBot(bot_token)


def split_message(text, max_lenght=4096):
    if text:
        if len(text) <= max_lenght:
            logger.debug('Сообщение меньше 4096 all good')
            return [text]
        logger.debug('Сообщение больше 4096 разбивка')
        lines = text.splitlines()
        parts = []
        current_part = ''
        for line in lines:
            if len(current_part) + len(line) + 1 <= max_lenght:
                current_part += line + '\n'
            else:
                parts.append(current_part.strip())
                current_part = line + '\n'
        if current_part:
            parts.append(current_part.strip())

        return parts


def send_message(message: list, links: str):
    """Отправка сообщений в Telegram"""
    if len(message) == 4:
        project_name, description, min_price, max_price = message

        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Перейти", url=links)
        keyboard.add(button)

        text = (f'<b>✨Название проекта</b>✨: {project_name}\n'
                f'<i>{description}</i>\n'
                f'<b>💸Минимальная цена💸</b>: {min_price} ₽\n'
                f'<b>💰Максимальная цена💰</b>: {max_price} ₽')

        prompt_replaced = prompt.replace('[title]', project_name).replace('[description]', description).replace('[min_budget]', min_price).replace('[max_budget]', max_price)

        ai_updated_message = client_data(prompt_replaced)
        text = text + f'\n<b>🤖Комментарий от нейросети🤖</b> {ai_updated_message}'
        splited_message = split_message(text)
        try:
            for msg in splited_message:
                bot.send_message(bot_group, msg, reply_markup=keyboard, parse_mode='HTML')
                logger.info(f"Сообщение успешно отправлено в чат {bot_group}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")


def start_bot():
    """Запуск бота в отдельном потоке"""
    bot.polling(none_stop=True)


def run_bot():
    """Запуск бота в фоне через поток"""
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()


if __name__ == "__main__":
    logger.info('🚀 Запуск программы')
    run_bot()
