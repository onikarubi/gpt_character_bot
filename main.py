from fastapi import FastAPI, Request, Response, status
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage
from dotenv import load_dotenv
import json

import pydantic
import os

load_dotenv('./.env')

class SamplePost(pydantic.BaseModel):
    x: int
    y: int


app = FastAPI()

line_bot_api = LineBotApi(os.getenv('LINE_BOT_API_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_BOT_API_SECRET'))

@app.get('/')
def root():
    return {'message': 'hello'}


@app.post('/')
def calc(data: SamplePost):
    result = data.x * data.y
    return result

@app.post('/callback')
async def callback(request: Request):
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()

    try:
        handler.handle(body.decode(encoding='utf-8'), signature)

    except InvalidSignatureError as error:
        print('署名に失敗しました')
        raise error

    return Response(status_code=status.HTTP_200_OK)

def reply_message_text(event: MessageEvent):
    msg_txt = event.message.text

    if not msg_txt:
        return

    if msg_txt == 'こんにちは':
        reply_message = 'Hello.'

    elif msg_txt == 'おはようございます' or msg_txt == 'おはよう':
        reply_message = 'Good morning.'

    elif msg_txt == 'こんばんは':
        reply_message = 'Good evening.'

    else:
        reply_message = 'Hello AI Bot'

    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=TextSendMessage(text=reply_message)
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    reply_message_text(event)

