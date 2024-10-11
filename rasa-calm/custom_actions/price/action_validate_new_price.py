import requests
import os

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import datetime

DOMAIN = os.getenv("DOMAIN")

class ActionValidateNewPrice(Action):
    def name(self):
        return "action_validate_new_price"

    def run(self, dispatcher, tracker, domain):
        #get language from metadata
        metadata = tracker.latest_message.get("metadata", {})
        language = metadata.get("language")

        new_price = tracker.get_slot('new_price')
        try:
            # Validate if new_price is a valid decimal number
            price = float(new_price)
            return [SlotSet("new_price_valid", True)]
        except ValueError:
            if language == "ar":
                dispatcher.utter_message("السعر الذي أدخلته غير صالح. يرجى إدخال قيمة رقمية صالحة.")
            else:
                dispatcher.utter_message("The price you entered is not valid. Please enter a valid numerical value.")
            return [SlotSet("new_price_valid", False)]