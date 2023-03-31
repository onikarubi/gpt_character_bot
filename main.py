from fastapi import FastAPI, Request, Response, status
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, ImageSendMessage, TextSendMessage
from apis.dall_e.image_model import ImageGenerator, ImageSize

import os

LINE_BOT_API_TOKEN = os.getenv('LINE_BOT_API_TOKEN')
LINE_BOT_API_SECRET = os.getenv('LINE_BOT_API_SECRET')

if LINE_BOT_API_TOKEN == None or LINE_BOT_API_SECRET == None:
    LINE_BOT_API_TOKEN = os.getenv('LINE_BOT_API_TOKEN')
    LINE_BOT_API_SECRET = os.getenv('LINE_BOT_API_SECRET')



app = FastAPI()

line_bot_api = LineBotApi(os.getenv('LINE_BOT_API_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_BOT_API_SECRET'))

@app.get('/')
def root():
    return {"message": 'hello'}

@app.post('/callback')
async def callback(request: Request):
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()

    try:
        handler.handle(body.decode(encoding='utf-8'), signature)

    except InvalidSignatureError as error:
        print('署名に失敗しました')
        raise error

    return {"status_code": Response(status_code=status.HTTP_200_OK), "content": body}

def reply_message(event: MessageEvent):
    msg_txt = event.message.text

    if not msg_txt:
        return

    if not msg_txt == '猫の画像':
        return

    image_generator = ImageGenerator(image_size=ImageSize(512, 512), prompt=msg_txt)
    response_url = image_generator.create_image()

    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=ImageSendMessage(original_content_url=response_url, preview_image_url=response_url)
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    if event.message.text == '猫の画像':
        reply_message(event)

    line_bot_api.reply_message(event.reply_token, messages=TextSendMessage(event.message.text))

