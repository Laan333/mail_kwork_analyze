import logging
import imaplib
import email
import threading
import time
from bs4 import BeautifulSoup
from work_w_env.envreader import EnvReader
from request_to_links.req_link import link_parser
from telegram_instrumentation.tg_sender import run_bot, send_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

reader = EnvReader()
reader.getter_env()

# Используем Event, чтобы основная программа жила, пока не завершится работа потока
exit_event = threading.Event()

def decode_part(part):
    """Декодирует содержимое письма"""
    payload = part.get_payload(decode=True) if part else None
    if not payload:
        logger.warning("⚠ Пустой payload, возможно, проблемы с кодировкой")
        return None

    return payload.decode('utf-8', errors='ignore')


def extract_links_from_html(body):
    """Извлекает все ссылки из HTML"""
    soup = BeautifulSoup(body, "html.parser")
    return [a['href'] for a in soup.find_all('a', href=True)]


def reformat_links(links):
    """Форматирование и обработка ссылок"""
    for link in links:
        clean_url = link.replace('new_offer?', '').split('"')[0].replace('3D', '').replace('=', 's/') + '/view'
        data = link_parser(clean_url)
        send_message(data, clean_url)


def fetch_emails():
    """Получение и обработка писем (СИНХРОННО)"""
    while not exit_event.is_set():  # Работает, пока не получен сигнал о завершении
        try:
            logger.info("📩 Проверяю почту...")

            # Создаем подключение к почте
            mail = imaplib.IMAP4_SSL(reader.imap)
            mail.login(reader.login, reader.password)
            mail.select('INBOX/Newsletters')

            # Поиск новых писем
            result, data = mail.search(None, '(UNSEEN FROM "{}")'.format(reader.sender_mail))
            if result != 'OK':
                mail.logout()
                time.sleep(1800)  # Если нет писем, ждём 30 минут
                continue

            links_list = []
            for email_id in data[0].split():
                result, msg_data = mail.fetch(email_id, '(RFC822)')
                if result != 'OK':
                    continue

                msg = email.message_from_bytes(msg_data[0][1])
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        decoded_body = decode_part(part)
                        if decoded_body:
                            links_list.extend([l for l in extract_links_from_html(decoded_body) if 'https://kwork.ru/new_offer' in l])

                mail.store(email_id, '+FLAGS', '\\Seen')  # Отмечаем письмо как прочитанное

            mail.logout()

            # Если найдены ссылки, обрабатываем их
            if links_list:
                reformat_links(links_list)

        except Exception as e:
            logger.error(f'Ошибка при обработке писем: {e}')
        timeout = 60 * 2
        logger.info(f'Ждем {timeout} секунд')
        time.sleep(timeout)

def main():
    """Запуск бота и обработчика писем в многопоточной среде"""
    email_thread = threading.Thread(target=fetch_emails, daemon=True)
    email_thread.start()

    logger.info('⏳ Ждем перед запуском потока почты...')
    run_bot()  # Запускаем бота в основном потоке

    # Ждем завершения потока обработки почты
    email_thread.join()

if __name__ == "__main__":
    logger.info('🚀 Запуск программы')
    main()
