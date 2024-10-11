import requests
import os

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import datetime

DOMAIN = os.getenv("DOMAIN")

class ActionModifyPrice(Action):

    def name(self) -> Text:
        return "action_modify_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #get language from metadata
        metadata = tracker.latest_message.get("metadata", {})
        language = metadata.get("language")
        
        # Extracting slots from the tracker
        project_id = tracker.get_slot("project_id")
        product_id = tracker.get_slot("product_id")
       
        item_id = tracker.get_slot("item_id")
        new_price = tracker.get_slot("new_price")  # Assuming new price is passed as a slot
        rollout_date = tracker.get_slot("rollout_date")  # Assuming rollout date is passed as a slot

        # Ensure required slots are filled
        if not all([project_id, product_id, item_id, new_price, rollout_date]):
            if language == "ar":
                dispatcher.utter_message(text="هناك بعض المعلومات الضرورية المفقودة لتعديل السعر.") 
            else:
                dispatcher.utter_message(text="Some necessary information is missing to modify the price.")
            return []

        # Convert rollout_date to ISO format
        try:
            # formatted_rollout_date = datetime.strptime(rollout_date, "%Y-%m-%d").isoformat() + ".000Z"
            # Parse the date string into a datetime object
            date_obj = datetime.strptime(rollout_date, "%Y-%m-%d")

            # Set the specific time to 04:00:00 and format it as required
            formatted_rollout_date = date_obj.replace(hour=4, minute=0, second=0, microsecond=0).isoformat(timespec='milliseconds') + "Z"

        except ValueError:
            if language == "ar":
                dispatcher.utter_message(text="تنسيق تاريخ الإطلاق غير صالح. يرجى تقديم تاريخ صالح بتنسيق YYYY-MM-DD.")
            else:
                dispatcher.utter_message(text="The rollout date format is invalid. Please provide a valid date in YYYY-MM-DD format.")
            return []

        # Current timestamp for lastUpdated field
        last_updated = datetime.now().isoformat()

        metadata = tracker.latest_message.get("metadata", {})
        cookies = metadata.get("cookies")
        xcsrf_token = metadata.get("X-Csrf-Token")


           # Construct the payload for the update price API request
        payloadForCustomPriceCreation = {
            "catalogName": "B2CCatalog",
            "projectId" : project_id,
            "productId" : product_id,
            "priceId" : item_id,
            "rolloverDate" :  rollout_date,
            "valueAmount" : new_price
        }


        # Perform the API POST request
        url = f"{DOMAIN}/service/stcui/UICustomAPI/customPriceCreation"
        headers = {
            "Cookie": cookies,
            "X-Csrf-Token": xcsrf_token
        }

        responseFromUpdatePrice = requests.post(url, json=payloadForCustomPriceCreation, headers=headers).json()
        dispatcher.utter_message(text="The price has been successfully modified with the Price Id" + responseFromUpdatePrice.get("newPriceId"))

        return [SlotSet("price_modified", True)]

