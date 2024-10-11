import requests
import os

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import datetime

DOMAIN = os.getenv("DOMAIN")

class ActionResetProductId(Action):
    def name(self):
        return "action_reset_product_id"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("product_id", None)]