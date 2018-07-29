### 一、	普通文字事件(Message event)
先看這段程式碼:  
---
def handle_message(event):  
	line_bot_api.reply_message(event.reply_token,  
		TextSendMessage(text="要回覆的話"))  
---
這段程式碼是伺服器收到使用者傳送訊息後執行的函式，  
收到的訊息是一個名叫"event"的事件。  
event裡重要的資料包含:  
"reply_token" : 回傳訊息時的密鑰，有時效性(很短)  
"type" : 代表本次事件的型態  
"source . user_id" : 使用者的ID(是程式配發的，與自己設定的ID不同)  
"message . text" : 使用者輸入的文字  
剩下的資料可在官網查詢(https://developers.line.me/en/reference/messaging-api/#message-event)  
第二行的line_bot_api . reply_message則會將訊息回覆給使用者，  
第一個參數輸入"reply_token"，第二個參數則輸入要回覆的訊息，  
而要回覆的訊息要用第三行的TextSendMessage(text="要回覆的話"))  
包裝成一個物件。

### 二、	回復多行訊息
由於通過Message event得到的密鑰"reply_token"只能使用一次，因此想要傳送多條訊息的話就必須使用主動推送功能"Push"。  
使用Push功能十分簡單，只要加上  
line_bot_api.push_message(user_id, 訊息物件)  
因此上面的程式可以修改為 :  
---
def handle_message(event):  
	line_bot_api.reply_message(event.reply_token,  
		TextSendMessage(text="要回覆的話"))  
	line_bot_api.push_message(user_id,  
		TextSendMessage(text="第二句話"))  
---
同理，再加上一行Push語法就可以說第三句話。

### 三、	特殊模板
使用特殊模板回覆與上面的文字回覆一樣，只是回傳的訊息物件不同而已。  
當使用者按下按鈕時，可以觸發Message, Postback, URL三種事件，  
Message事件會主動幫使用者輸入某一句話，然後觸發第一篇的Message Event。  
Postback事件會觸發Postback Event，讓在使用者什麼都沒輸入的情況下觸發另一事件，這個部份我們後面再解釋。  
URL事件則會引導使用者開啟一個網頁。  

#### 1. 確認介面訊息(Confirm Template)  
---
message = TemplateSendMessage(  
    alt_text='當畫面無法呈現時的替代文字(如電腦版)',  
    template=ConfirmTemplate(  
        text='上半部的文字(如上圖的Make a reservation?)',  
        actions=\[  
            PostbackTemplateAction(  
                label='按鈕上的文字',  
                text='使用者按下按鈕後會回覆的話',  
                data='觸發Postback時夾帶的資料'  
            ),  
            MessageTemplateAction(  
                label='按鈕上的文字',  
                text='按下按鈕後使用者回覆的話'  
            )  
        \]  
    )  
)  
line_bot_api.reply_message(event.reply_token, message)  
---
