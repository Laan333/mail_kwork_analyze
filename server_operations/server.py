from fastapi import FastAPI, WebSocket
import asyncio
import logging
from ai_operations.connection_ai import client_data
from ai_operations.lexicon_for_ai import prompt
from request_to_links import req_link

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI()
connections = set()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        connections.remove(websocket)


@app.post('/send_data/')
async def send_data(data: list[dict]):
    logger.info('Сообщение на сервере получено. Начинаем обработку')
    all_data_for_send: list = []
    for i in range(len(data)):
        project_data: list = await req_link.link_parser(data[i]['link'])  # Парсим ссылку
        text_for_ai = prompt.replace('[title]', project_data[0]).replace('[description]', project_data[1]).replace('[min_budget]', project_data[2]).replace('[max_budget]', project_data[3])
        logger.info(f'{text_for_ai} - cообщение нейросети')
        result: str = client_data(text_for_ai)  # Отправляем текст в нейросеть
        logger.info('Нейросеть ответила, all good')
        all_data_for_send.append({'link': data[i]['link'],'scraped_info': project_data, 'ai_answer':result})
    logger.info('Все сообщения были собраны,прослушиваем...')
    await asyncio.gather(*(conn.send_json(all_data_for_send) for conn in connections))


    return {'status': 'OK'}
