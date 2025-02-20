import asyncio
import websockets
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def listen(queue):
    uri = "ws://localhost:8000/ws"

    while True:  # Бесконечный цикл для попыток переподключения
        try:
            logger.info(f'Попытка подключения к {uri}')
            async with websockets.connect(uri) as websocket:
                logger.info('Соединение установлено')
                await websocket.send("connect")

                while True:  # Бесконечный цикл для получения сообщений
                    message = await websocket.recv()
                    try:
                        data = json.loads(message)
                        logger.info(f'Данные получены: {data} и отправляем их в очередь')
                        queue.put(data)  # Отправляем данные в очередь
                    except json.JSONDecodeError:
                        logger.info(f"📩 Получено текстовое сообщение: {message}")
                        queue.put(message)  # Отправляем текстовое сообщение в очередь
        except websockets.exceptions.WebSocketException as e:
            logger.error(f"Ошибка соединения: {e}")
            logger.info("Попытка переподключения через 5 секунд...")
            await asyncio.sleep(5)  # Задержка перед попыткой повторного подключения