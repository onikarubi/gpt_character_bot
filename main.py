from fastapi import FastAPI, Request, Response, status
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.exceptions import LineBotApiError
from linebot.models import TextMessage, MessageEvent, ImageSendMessage, TextSendMessage
from apis.dall_e.image_model import ImageGenerator, ImageSize
from logs.line_api_access import line_logger_output
import os

LINE_BOT_API_TOKEN = os.getenv('LINE_BOT_API_TOKEN')
LINE_BOT_API_SECRET = os.getenv('LINE_BOT_API_SECRET')


app = FastAPI()

line_bot_api = LineBotApi(os.getenv('LINE_BOT_API_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_BOT_API_SECRET'))


@app.post('/callback')
async def callback(request: Request):
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()

    try:
        handler.handle(body.decode(encoding='utf-8'), signature)
        line_logger_output(level='info', message='署名に成功しました')

    except InvalidSignatureError:
        line_logger_output(level='error', message='署名に失敗しました')
        raise

    except AttributeError:
        line_logger_output(level='error', message='署名に失敗しました。署名の設定を見直して下さい')
        raise

    return {"status_code": Response(status_code=status.HTTP_200_OK), "content": body}


def reply_message_image(event: MessageEvent, req_test = False):
    if not event.message.text == '猫の画像':
        return

    if req_test:
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=ImageSendMessage(original_content_url='dummy_original_content_url', preview_image_url='dummy_preview_image_url'))
        print('※ 検証用のリクエスト内容を作成しています。')
        return

    image_generator = ImageGenerator(
        image_size=ImageSize(512, 512), prompt=event.message.text)

    response_url = image_generator.create_image()

    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=ImageSendMessage(
            original_content_url=response_url, preview_image_url=response_url)
    )

def reply_message_text(event: MessageEvent):
    if not event.message.text:
        return

    line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(event.message.text))


@handler.add(MessageEvent, message=TextMessage)
def handle_message_text(event: MessageEvent, req_test = False):
    try:
        if event.message.text == '猫の画像':
            reply_message_image(event, req_test=req_test)
            return

        reply_message_text(event)

    except:
        error_msg = 'Line bot上で問題が発生しました。'
        raise LineBotApiError(error_msg)
