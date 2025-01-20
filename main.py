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


configuration = Configuration(access_token=os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(channel_secret=os.environ["CHANNEL_SECRET"])

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


@handler.add(BeaconEvent, message=BeaconContent)
def handle_beacon(event, beacon_content):
    line_bot_api.reply_message(
        event.reply_token,
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(
                    text="Got beacon event type={} from hwid={}".format(
                        beacon_content.type, beacon_content.hwid
                    )
                )
            ],
        ),
    )
