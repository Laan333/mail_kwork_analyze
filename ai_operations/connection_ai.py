import json
import logging
import os

import requests
import dotenv
from ai_operations import lexicon_for_ai
dotenv.load_dotenv()


logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

def client_data(message_text:str):
    url = os.getenv('url')
    data = {
        "model": "qwen2.5:32b",  # Укажите вашу модель
        "prompt": message_text,  # Ваш запрос
        "stream": True,  # Установите stream в True
    }

    try:
        logger.info('Try to send data to AI')
        # Выполняем POST-запрос
        response = requests.post(url, json=data, stream=True)
    except Exception as e:
        logger.error(f'Cant do that. Error: {e} (Проблема в нейросетке)')
        return False
    logger.info('Request sended succesfuly')
    full_response = ""
    # Обрабатываем потоковые данные
    for chunk in response.iter_lines():
        if chunk:
            try:
                # Декодируем JSON-строку в словарь
                json_data = json.loads(chunk.decode('utf-8'))

                # Извлекаем текст ответа из полученного словаря
                response_part = json_data.get("response", "")
                full_response += response_part  # Собираем все части в одну строку
            except Exception as e:
                logger.error(f"Error while processing chunk: {e}")
    logger.info('Message formated succesfuly')
    return full_response
