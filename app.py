from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import random

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('LYU17p/05jfJVP9/qFJSDy9UehswxFb+lJr9B1RBC4yu8Btp8e5bUZVRqZAsBm/21u/OfjxDt/HkObxp1LCsv43q1+wqvsOnLML4EGYKJrnLv0X1qEMvsjCxZPm2spLSs/ygc6zYVDE62F5/gT3YXwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('ac6df3f9df4d72cdf75eda9d0a7ae488')

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

card = ['大吉`只要時常保持微笑，\n全世界的好運都會跑到你的身邊呢!',
            '大吉`待人和善的你就像行走在世間的天使，\n又何須擔心甚麼厄運呢?',
            '吉`若是感覺到了身邊的人帶給你的愛，\n記得也送他們一個大大的笑容喔!',
            '吉`只要相信自己，\n沒有我們做不到的事!',
            '平`若是生活一如往常，\n不也是一件好事嗎?',
            '凶`凡事宜謹慎，勿躁進',
            '大凶`無論遇到什麼事情，\n都不要忘了與你同在的人們']

def PickCard():
    message = TemplateSendMessage(
        alt_text='占星牌(手機限定)',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://lh5.googleusercontent.com/4WYOIBDNVD6E-4IaH6u8D2JIpmbWOKla4NK_B6P6WajRyc7cgocqS70iR4ZRxOY6rDeif22t7bzM1cyos60Z=w1920-h931',
                    title='占星卡',
                    text='抽一張吧!',
                    actions=[
                        PostbackTemplateAction(
                            label='抽卡',
                            data='抽卡`' + str(random.randint(0,len(card)-1))
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://lh5.googleusercontent.com/4WYOIBDNVD6E-4IaH6u8D2JIpmbWOKla4NK_B6P6WajRyc7cgocqS70iR4ZRxOY6rDeif22t7bzM1cyos60Z=w1920-h931',
                    title='占星卡',
                    text='抽一張吧!',
                    actions=[
                        PostbackTemplateAction(
                            label='抽卡',
                            data='抽卡`' + str(random.randint(0,len(card)-1))
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://lh5.googleusercontent.com/4WYOIBDNVD6E-4IaH6u8D2JIpmbWOKla4NK_B6P6WajRyc7cgocqS70iR4ZRxOY6rDeif22t7bzM1cyos60Z=w1920-h931',
                    title='占星卡',
                    text='抽一張吧!',
                    actions=[
                        PostbackTemplateAction(
                            label='抽卡',
                            data='抽卡`' + str(random.randint(0,len(card)-1))
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://lh5.googleusercontent.com/4WYOIBDNVD6E-4IaH6u8D2JIpmbWOKla4NK_B6P6WajRyc7cgocqS70iR4ZRxOY6rDeif22t7bzM1cyos60Z=w1920-h931',
                    title='占星卡',
                    text='抽一張吧!',
                    actions=[
                        PostbackTemplateAction(
                            label='抽卡',
                            data='抽卡`' + str(random.randint(0,len(card)-1))
                        )
                    ]
                ),
                CarouselColumn(
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
            ]
        )
    )
    return message
    

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, PickCard())

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
