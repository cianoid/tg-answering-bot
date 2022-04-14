import os
import re

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
GROUP_ID = os.environ.get('GROUP_ID')


app = Client("my_account", API_ID, API_HASH)


@app.on_message()
def new_message(client, message):
    if message.outgoing is False and message.chat.type == 'private':
        if re.search('(:?^|[^а-я])барахолк[иау]', message.text, re.IGNORECASE):
            app.send_message(
                chat_id=message.from_user.id,
                reply_to_message_id=message.message_id,
                text=(
                    'Добрый день! Это автоматический ответ. Вход в '
                    'барахолку по скриншоту из ЛК ПИК'))


app.run()
