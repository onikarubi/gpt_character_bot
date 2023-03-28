from fastapi import FastAPI, Request, Response, status
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, ImageSendMessage
from apis.dall_e.image_model import ImageGenerator, ImageSize

import pydantic
import os

LINE_BOT_API_TOKEN = os.getenv('LINE_BOT_API_TOKEN')
LINE_BOT_API_SECRET = os.getenv('LINE_BOT_API_SECRET')

def load_env_file():
    from dotenv import load_dotenv

    load_dotenv('./.env')

if LINE_BOT_API_TOKEN == None or LINE_BOT_API_SECRET == None:
    load_env_file()
    LINE_BOT_API_TOKEN = os.getenv('LINE_BOT_API_TOKEN')
    LINE_BOT_API_SECRET = os.getenv('LINE_BOT_API_SECRET')


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

def reply_message_image(event: MessageEvent):
    msg_txt = event.message.text

    if not msg_txt:
        return

    image_generator = ImageGenerator(image_size=ImageSize(512, 512), prompt=msg_txt)
    response_url = image_generator.create_image()

    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=ImageSendMessage(original_content_url=response_url, preview_image_url=response_url)
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    reply_message_image(event)

