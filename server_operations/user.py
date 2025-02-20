import requests
import json


def send_data(data: list[dict]):
    """
    Отправляет данные на WebSocket сервер через POST запрос.

    Args:
        data (dict): Словарь с данными для отправки.

    Returns:
        dict: Ответ сервера.
    """
    url = 'http://localhost:8000/send_data/'

    try:

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Вызовет исключение, если статус не 2xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке данных: {e}")
        return None


