import sqlite3
import datetime

from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
)

con = sqlite3.connect("line_user.db")


def get_user_demographic():
    pass

def generate_flex_message_by_user_demographic(user_id):
    member = get_user_demographic(user_id)
    if not member:
        flex_msg = open("flex_templates/cj_register_sabai_card.json").read()
    else:
        dob = datetime.strptime(member["dob"], "%Y-%m-%d")
        today = datetime.today()
        member_age = (
            today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        )

        if (member_age > 30) and (member["gender"] == "male"):
            flex_msg = open("flex_templates/male_car_lover.json").read()
        elif (member_age > 30) and (member["gender"] == "female"):
            flex_msg = open("flex_templates/women_items_promotion.json").read()
        elif (member_age <= 30) and (member["gender"] == "male"):
            flex_msg = open("flex_templates/boy_toy_gaming.json").read()
        elif (member_age <= 30) and (member["gender"] == "female"):
            flex_msg = open("flex_templates/girl_cosmetics_promotion.json").read()

    return FlexMessage(
        alt_text="personalized_message_from_beacon",
        contents=FlexContainer.from_json(flex_msg),
    )
    
def generate_flex_message_by_hwid(hwid):
    flex_msg = open("flex_templates/station_beacon.json").read()
    if hwid == "00000ac697":
        station_01_flex_msg = (
            flex_msg.replace("<NAME>", "วัดพระแก้ว").replace("<IMAGE_URL>","")
        )
        return FlexMessage(
            alt_text="วัดพระแก้ว",contents=FlexContainer.from_json(station_01_flex_msg),
        )
    elif hwid == "00000ab000":
        station_02_flex_msg = (
            flex_msg.replace("<NAME>", "วัดพระแก้ว").replace("<IMAGE_URL>","")
        )
        return FlexMessage(
            alt_text="personalized_message_from_beacon", contents=FlexContainer.from_json(station_02_flex_msg),
        )
    elif hwid == "00000ab001":
        station_03_flex_msg = (
            flex_msg.replace("<NAME>", "ภูเขาทอง วัดสระเกศ ราชวรมหาวิหาร").replace("<IMAGE_URL>","https://cms.dmpcdn.com/travel/2023/07/21/b49e90f0-277d-11ee-bd8c-75c68f6ec73a_webp_original.webp")
        )
        return FlexMessage(
            alt_text="ภูเขาทอง วัดสระเกศ ราชวรมหาวิหาร", contents=FlexContainer.from_json(station_03_flex_msg),
        )
        
def get_event_flex_message(event_name):
    if event_name == "data_and_ai" :
        flex_msg = open("flex_templates/flex_event_template.json").read()
        return FlexMessage(
            alt_text="personalized_message_from_beacon",
            contents=FlexContainer.from_json(flex_msg),
        )
        