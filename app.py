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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    find = False
    with open("user_dic",'r') as f:
	    for u in f.readlines():
            user = u.strip().split('~')
            if user[1] == event.source.user_id && user[0] != '!' :
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user[0]+"你好"))
                find = True
                break
            elif user[1] == event.source.user_id && user[0] == '!' :
                find = True
                message = TemplateSendMessage(
                    alt_text='姓名確認',
                    template=ConfirmTemplate(
                        text='您叫做'+event.message.text+'對嗎',
                        actions=[
                            PostbackTemplateAction(
                                label='不對',
                                data='wrong'
                            ),
                            PostbackTemplateAction(
                                label='對',
                                data='right~'+event.message.text
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, message)
    if !find : 
        with open("user_dic",'a') as f:
            f.write(event.source.user_id + '~!\n')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='初次使用請輸入你的姓名'))


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data.split('~')[0] == 'wrong':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請再次輸入您的姓名'))
    elif event.postback.data.split('~')[0] == 'right':
        userlist = []
        with open("user_dic",'r') as f:
            userlist = f.readlines
            for u in userlist:
                if u.strip().split('~')[1] == event.source.user_id:
                    u = u.strip().split('~')[0] + event.postback.data.split('~')[1] +'\n'
                    break
        with open("user_dic",'w') as f:
            for u in userlist:
                f.write(u)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='儲存成功'))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
