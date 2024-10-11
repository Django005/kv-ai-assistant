import requests
import os

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import datetime

DOMAIN = os.getenv("DOMAIN")

class ActionSetLanguage(Action):
    def name(self):
        return "action_set_language"

    def run(self, dispatcher, tracker, domain):
        metadata = tracker.latest_message.get("metadata", {})
        language = metadata.get("language")
        return [SlotSet("language", language)]
       