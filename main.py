import logging
from server_operations.user import send_data
from work_w_env.envreader import EnvReader

import imaplib
import email
import re
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

reader = EnvReader()
reader.getter_env()



def extract_links(text):
    """ Извлекает ссылки из текста """
    return re.findall(r'(https?://\S+)', text)


def transform_link(link):
    """ Преобразует ссылку с project= в нужный формат """
    match = re.search(r'project=(\d+)', link)
    if match:
        project_id = match.group(1)
        return f"https://kwork.ru/projects/{project_id}/view"
    return None


def process_emails(mail, sender):
    """Обрабатывает непрочитанные письма и извлекает нужные ссылки"""
    result, data = mail.search(None, '(UNSEEN FROM "{}")'.format(sender))
    email_ids = data[0].split()
    logger.info(f'Были найдены письма {email_ids}')
    for email_id in email_ids:
        result, email_data = mail.fetch(email_id, '(RFC822)')
        try:
            raw_email = email_data[0][1]
        except Exception as e:
            logger.error(f"Ошибка получения письма {email_id}: {e}")
            continue

        msg = email.message_from_bytes(raw_email)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type in ['text/plain', 'text/html']:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode(charset, errors='replace')
                    except Exception as e:
                        logger.info(f'Ошибка декодирования письма: {e}')
        else:
            charset = msg.get_content_charset() or 'utf-8'
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(charset, errors='replace')
            except Exception as e:
                logger.info(f'Ошибка декодирования письма: {e}')

        # Извлекаем ссылки и преобразуем их
        links = extract_links(body)
        transformed_links = []
        for link in links:
            t_link = transform_link(link)
            if t_link:
                transformed_links.append({'link': t_link})

        if transformed_links:
            logger.info('Отправляем ссылки на сервер...')
            send_data(transformed_links)
        else:
            logger.info("Нет подходящих ссылок.")

        # Помечаем письмо как прочитанное
        mail.store(email_id, '+FLAGS', '\\Seen')
        logger.info(f'Сообщение {email_id} прочитано')


def main():
    """ Основной цикл работы с почтой """
    mail = imaplib.IMAP4_SSL(reader.imap)
    mail.login(reader.login, reader.password)
    mail.select('INBOX/Newsletters')
    logger.info('Скрипт запущен')
    sender = reader.sender_mail
    logger.info(f"Ищем письма {sender}")
    logger.info(f'{reader.sender_mail}')
    while True:
        process_emails(mail, sender)
        time.sleep(60)


if __name__ == '__main__':
    main()

