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
    userdict = {}
    with open("user_dic",'r') as f:
        userdict = eval(f.readline().strip())
        
    try:
        if userdict[event.source.user_id] != 'none':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您好'+userdict[event.source.user_id]))
        else:
            message = TemplateSendMessage(
                alt_text='特殊訊息(手機版限定)',
                template=ConfirmTemplate(
                    text='您叫做'+event.message.text+'對嗎?',
                    actions=[
                        PostbackTemplateAction(
                            label='對',
                            data='right~'+event.message.text
                        ),
                        PostbackTemplateAction(
                            label='不是',
                            data='wrong~'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
    except:
        userdict[event.source.user_id] = 'none'
        with open("user_dic",'w') as f:
            w.write(str(userdict))
    
@handler.add(PostbackEvent)
def handle_postback(event):
    userdict = {}
    with open("user_dic",'r') as f:
        userdict = eval(f.readline().strip())
        
    if event.postback.data.split('~')[0] == 'wrong':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請再次輸入您的姓名'))
    elif event.postback.data.split('~')[0] == 'right':
        userdict[event.source.user_id] = event.postback.data.split('~')[1]
        with open("user_dic",'w') as f:
            w.write(str(userdict))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='儲存成功'))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
