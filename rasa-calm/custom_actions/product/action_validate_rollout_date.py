import requests
import os

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import datetime

DOMAIN = os.getenv("DOMAIN")

class ActionValidateRolloutDate(Action):
    def name(self):
        return "action_validate_rollout_date"

    def run(self, dispatcher, tracker, domain):
        #get language from metadata
        metadata = tracker.latest_message.get("metadata", {})
        language = metadata.get("language")
        

        rollout_date = tracker.get_slot('rollout_date')
        try:
            # Accept any format and convert to UTC
            return [SlotSet("rollout_date_valid", True), SlotSet("rollout_date", rollout_date)]
        except ValueError:
            if language == "ar":
                dispatcher.utter_message("التاريخ الذي أدخلته غير صالح. يرجى إدخال تاريخ صالح بالتنسيق YYYY-MM-DD.")
            else:
                dispatcher.utter_message("The date you entered is not valid. Please enter a valid date in the format YYYY-MM-DD.")
            return [SlotSet("rollout_date_valid", False)]