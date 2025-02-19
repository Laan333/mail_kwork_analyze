import logging
import os

import dotenv

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)



class EnvReader():
    dotenv.load_dotenv()

    def __init__(self):
        self.imap = None
        self.login = None
        self.password = None
        self.sender_mail = None


    def getter_env(self):
        self.imap = os.getenv('imap_server')
        self.login = os.getenv('email')
        self.password = os.getenv('password')
        self.sender_mail = os.getenv('sender')



