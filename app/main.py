import logging
import os
import re

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
GROUP_ID = os.environ.get('GROUP_ID')


logger = logging.getLogger(__name__)


class EnvironmentParameterError(Exception):
    pass


def log_init():
    logs_directory = os.path.join(os.getcwd(), 'logs')
    log_level = os.environ.get('LOG_LEVEL', default='INFO')

    if not os.path.isdir(logs_directory):
        os.mkdir(logs_directory)
    filename = os.path.join(logs_directory, '%s.log' % log_level.lower())

    logging.basicConfig(
        filename=filename, filemode='a', level=log_level,
        format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)s - '
               '%(funcName)s()] %(message)s',
        datefmt='%d.%m.%y %T%z')

    logging.info('Logger initialized')


def environment_check():
    try:
        logger.debug('Проверка env-переменных для подключения')

        if API_ID is None:
            raise EnvironmentParameterError('API_ID')
        if API_HASH is None:
            raise EnvironmentParameterError('API_HASH')
    except EnvironmentParameterError as parameter:
        logger.critical(
            'Отсутствует обязательная переменная "{parameter}". Бот '
            'остановлен'.format(parameter=parameter))
        raise SystemExit


log_init()
environment_check()

app = Client("my_account", API_ID, API_HASH)


@app.on_message()
def new_message(client, message):
    if not (message.outgoing is False and message.chat.type == 'private'):
        return False

    regexp = '(:?^|[^а-я])барахолк[иау]'

    if not re.search(regexp, message.text, re.IGNORECASE):
        return False

    answer = ('Добрый день!\nВход в чат Барахолка ЖК Жулебино Парк '
              'осуществляется по скриншоту из Личного Кабинета ПИК, '
              'ПИК-Комфорт, ПИК-Домофон.\nЭто автоматический ответ в тестовом '
              'режиме')

    log_message = (
        'Пользователь {last_name} {first_name} (@{username}, id={id}) '
        'отправил сообщение с текстом "{message_text}"\nТекст автоматического '
        'ответа: "{answer}"'.format(
            last_name=message.from_user.last_name,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
            id=message.from_user.id, message_text=message.text, answer=answer))

    logger.info(log_message)

    app.send_message(
        chat_id=message.from_user.id,
        reply_to_message_id=message.message_id,
        text=answer)

    app.send_message('me', log_message)


app.run()
