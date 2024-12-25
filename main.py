import os
import functions_framework

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    BeaconEvent,
    BeaconContent,
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    FlexMessage,
    FlexContainer,
    TextMessage,
)



CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

configuration = Configuration(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)


@functions_framework.http
def callback(request):
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )

    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event, message):
    line_bot_api.reply_message(
        event.reply_token,
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=message.text)],
        )
    )
    

    
@handler.add(BeaconEvent, message=BeaconContent)
def handle_beacon(event, message):
    line_bot_api.reply_message(
        event.reply_token,
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=message.type)],
        )
    )

