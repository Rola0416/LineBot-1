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
    if event.message.text == '占星卡':
        line_bot_api.reply_message(event.reply_token, PickCard())
    elif event.message.text == '讚喔':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='謝謝你的支持，Have a nice day.'))

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data.split('`')
    if data[0] == '抽卡':
        i = int(data[1])
        c = card[i].split('`')
        
        if c[0] == '大吉':
            url = 'https://lh3.googleusercontent.com/ecSKhVOu1bnl_O0BGd_l4EVdwko6vZVHQflVaDxCNIoTCF94xev8d6o6OXRziew2zyQWfKMDPrZd13N0m95q=w1920-h931-rw'
        elif c[0] == '吉':
            url = 'https://lh3.googleusercontent.com/adUIxDSsvc7U8_wFzgmrWXQypLHuyGkZWj4xzTaV-oWXv9xQ8xfq4nMHKqJ9PzdRKEpX3381HT3VkjhOKE_u=w1920-h931-rw'
        elif c[0] == '平':
            url = 'https://lh3.googleusercontent.com/r1b8IY5WvZ68IC0B4lmok4gwNSAAVHFj8PwkcLTetUyZznVzDtX8cw2NYLYke1W8q3Fw0aHrvERXzjG5Zow_=w1920-h931-rw'
        elif c[0] == '凶':
            url = 'https://lh3.googleusercontent.com/Tn5VNq9KIf_Wjtj7ALus0k5J-OpmqEEAKswgKuerrOr1whHK76iVSGyRVoHlKOW_9xIE4J0CiJM7ayltRZWS=w1920-h931-rw'
        elif c[0] == '大凶':
            url = 'https://lh4.googleusercontent.com/dhDEM83DVpZltvmtPeRXtbpJeBwgujkmO5OHkHcr2PRBlkT3n9lzA9d7vni-Kod5pnLEG9tH5rENAPoRcxGn=w1920-h931-rw'
        message = TemplateSendMessage(
            alt_text='占星卡(手機限定)',
            template=ButtonsTemplate(
                thumbnail_image_url=url,
                title=c[0],
                text=c[1],
                actions=[
                    MessageTemplateAction(
                        label='讚',
                        text='讚喔'
                    )
                ]
            )
        )
line_bot_api.reply_message(event.reply_token, message)
        
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
