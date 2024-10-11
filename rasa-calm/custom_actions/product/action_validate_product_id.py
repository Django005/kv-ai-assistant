import requests
import os

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import datetime

DOMAIN = os.getenv("DOMAIN")

class ActionValidateProductID(Action):
    def name(self) -> Text:
        return "action_validate_product_id"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:

        #get language from metadata
        metadata = tracker.latest_message.get("metadata", {})
        language = metadata.get("language")

        product_id = tracker.get_slot("product_id")
        # hardcoded project name for development purposes
        project_id = tracker.get_slot("project_id")
        
        # if user has not given product id, then return None for validity
        if not product_id:
            return [SlotSet("product_id_valid", False)]

        metadata = tracker.latest_message.get("metadata", {})
        cookies = metadata.get("cookies")
        xcsrf_token = metadata.get("X-Csrf-Token")
        
        ## TODO // move this to environment file
        ## this can be any domain in the future
        ## separate the domain from actual end point
        ## domain must comes from environment file
        get_product_details_url = f"{DOMAIN}/service/catalog/plm/getProjectItem"

        payload = {
            "projectItemRequest": {
                "projectId":project_id,
                "itemId":product_id,
                "itemType":"PRODUCT",
                "__metadata": {
                    "type":"com.kloudville.catalog.plm.projectItemRequest"
                }
            }
        }

        headers = {
            "Cookie": cookies,
            "X-Csrf-Token": xcsrf_token
        }
        
        try:
            response = requests.post(get_product_details_url, json=payload, headers=headers)
            data = response.json()

            # safety fallback in case data is empty
            if data is None:
                if language == "ar":
                    dispatcher.utter_message(text="تعذر الوصول إلى تفاصيل المنتج")
                else:
                    dispatcher.utter_message(text="Could not access product details")
                return [SlotSet("product_id_valid", False)]

            # if there is an error message in data object
            if data.get('message') and data['message'].get('text'):
                return [SlotSet("product_id_valid", False)]
            

            if data.get('projectItem') and data['projectItem'].get('item'):
                # Extracting values from the response data
                old_price_id = data.get("projectItem", {}).get("item", {}).get("priceId")
                new_price_version_id = data.get("projectItem", {}).get("item", {}).get("nextPriceVersion")
                old_version_id = data.get("projectItem", {}).get("item", {}).get("versionId")
                new_price_version_code = data.get("projectItem", {}).get("item", {}).get("nextPriceVersionCode")
                product_category = data.get("projectItem", {}).get("item", {}).get("productCategory")
                path = data.get("projectItem", {}).get("item", {}).get("path")

                # Setting the slots with extracted values
                return [
                    SlotSet("product_id_valid", True),
                    SlotSet("old_price_id", old_price_id),
                    SlotSet("new_price_version_id", new_price_version_id),
                    SlotSet("old_version_id", old_version_id),
                    SlotSet("new_price_version_code", new_price_version_code),
                    SlotSet("product_category", product_category),
                    SlotSet("path", path)
                ]

            

        except Exception as e:
            print("Error in validation")
            print(e)
            if language == "ar":
                dispatcher.utter_message(text="حدث خطأ أثناء استرداد تفاصيل المنتج. يرجى المحاولة مرة أخرى في وقت لاحق.")
            else:
                dispatcher.utter_message(text="Error retrieving product details. Please try again later.")
            return []
        