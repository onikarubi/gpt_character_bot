from fastapi import FastAPI, Request, Response, status
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import TextMessage, MessageEvent, ImageSendMessage, TextSendMessage
from apis.linebot.linebot import LineBotReplyText, LineBotReplyImage, LineBotHandler
from apis.openai.gpt.llm_gpt import GPT3ChatFactory
import logs.request_logger
import os

LINE_BOT_API_TOKEN = os.getenv('LINE_BOT_API_TOKEN')
LINE_BOT_API_SECRET = os.getenv('LINE_BOT_API_SECRET')


app = FastAPI()

line_bot_handler = LineBotHandler(
    api_token=LINE_BOT_API_TOKEN,
    api_secret=LINE_BOT_API_SECRET
)

@app.post('/callback')
async def callback(request: Request):
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()

    try:
        line_bot_handler.webhook_handler.handle(body.decode(encoding='utf-8'), signature)
        logs.request_logger.logger_output(level='info', message='署名が完了しました')

    except InvalidSignatureError:
        logs.request_logger.logger_output(level='error', message=f'署名に失敗しました: {callback}')
        raise

    except AttributeError:
        logs.request_logger.logger_output(
            level='error', message=f'署名に失敗しました: {callback}\n署名の設定を見直して下さい')
        raise

    return {"status_code": Response(status_code=status.HTTP_200_OK), "content": body}


def reply_message_image(event: MessageEvent, test_mode=False):
    reply_message = LineBotReplyImage(
        api_token=LINE_BOT_API_TOKEN,
        api_secret=LINE_BOT_API_SECRET,
        test_mode=test_mode
    )

    reply_message.reply_message(event)


def reply_message_text(event: MessageEvent):
    content = GPT3ChatFactory.output_prompt(input_prompt=event.message.text)
    reply_message = LineBotReplyText(
        api_token=LINE_BOT_API_TOKEN,
        api_secret=LINE_BOT_API_SECRET,
        text_content=content
    )

    reply_message.reply_message(event)


@line_bot_handler.webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message_text(event: MessageEvent, test_mode = False):
    try:
        if event.message.text == '猫の画像':
            reply_message_image(event, test_mode=test_mode)
            return

        reply_message_text(event)

    except:
        error_msg = 'Line bot上で問題が発生しました。'
        raise LineBotApiError(error_msg)
