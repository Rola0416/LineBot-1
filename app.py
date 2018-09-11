from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('vlgEBYCHqjedWeOr0LghZpXN7KALtdXebquusc3WHQOPBwEGujQZ0c/fbA51Kb4kyHvJ335W8D35WeORu7i26jnjYK7T4Nuf5jLhZvByrEnIDggnhcbT1Jdaw6b5TWsrfIiGn3XKuvNHn3z1yVE9lQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('dfaf82e2cd7fae694b3d6fc9bc691dac')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

a = CarouselColumn(
    thumbnail_image_url='https://lh5.googleusercontent.com/4WYOIBDNVD6E-4IaH6u8D2JIpmbWOKla4NK_B6P6WajRyc7cgocqS70iR4ZRxOY6rDeif22t7bzM1cyos60Z=w1920-h931',
    title='占星卡',
    text='抽一張吧!',
    actions=[
        PostbackTemplateAction(
            label='抽卡',
            data='抽卡`' + str(random.randint(0,len(card)-1))
        )
    ]
)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TemplateSendMessage(
        alt_text='占星牌(手機限定)',
        template=CarouselTemplate(
            columns=[
                a,a,a
            ]
        )
    )
    return message

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
