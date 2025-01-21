import os
import functions_framework

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    BeaconEvent,
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    ShowLoadingAnimationRequest,
    TextMessage,
)

from generate_reply_message import (
    generate_flex_message_by_user_demographic,
    generate_flex_message_by_hwid,
    get_event_flex_message,
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


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    line_bot_api.show_loading_animation(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )

    text = event.message.text
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(text=text),
            ],
        )
    )


@handler.add(BeaconEvent)
def handle_beacon(event: BeaconEvent):

    text_message = (
        TextMessage(
            text="Got beacon event type={} from hwid={}".format(
                event.beacon.type, event.beacon.hwid
            )
        ),
    )

    flex_message_by_user_demographic = generate_flex_message_by_user_demographic(
        event.source.user_id
    )
    
    flex_message_by_hardwear_id = generate_flex_message_by_hwid(
        event.beacon.hwid
    )
    
    flex_event_message = get_event_flex_message(event_name="data_and_ai")



    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                text_message,
                # flex_message_by_user_demographic,
                # flex_message_by_hardwear_id,
                # flex_event_message
            ],
        ),
    )
