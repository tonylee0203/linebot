from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='Bor8Y++cwWE7QqiQtWAr0uqvNXWQ0u4KOn7Ya5VqbuHvxAsAqaGtWb+WUMytj/gArpcsdxzLSAiUiMXwSJczs24t1Ayj+iHL409vORBVNdnuTtrSaWfv7zJCwMNIdGYmsDcqDe3NeiD8/NfwKesE0AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('53174ba0559d891e34ef648512481215')


@app.route("/", methods=['POST'])
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_msg = event.message.text
    reply_msg = '你好,我是蘋果哥'

    if user_msg in [ 'hi','Hi','你好','您好','hello','Hello']:
        reply_msg = '您好'
    elif user_msg in ['菜單','請問菜單','menu','請問menu']:
        reply_msg = '我們提供巧克力蛋糕,熱可可,冰咖啡等'
    elif '飲料' in user_msg:
        reply_msg = '我們提供熱可可,冰咖啡,紅茶等'
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)        
        r = ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_msg)]
            )
        line_bot_api.reply_message_with_http_info(r)


if __name__ == "__main__":
    app.run()
