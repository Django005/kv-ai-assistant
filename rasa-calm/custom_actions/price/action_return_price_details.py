import requests
import os

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import datetime

DOMAIN = os.getenv("DOMAIN")

class ActionReturnPriceDetails(Action):
    def name(self) -> Text:
        return "action_return_price_details"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:

        #get language from metadata
        metadata = tracker.latest_message.get("metadata", {})
        language = metadata.get("language")

        product_id = tracker.get_slot("product_id")
        # hardcoded project name for development purposes
        project_id = tracker.get_slot("project_id")
        
        # if user has not given product id, then return None for validity
        if not product_id:
            dispatcher.utter_message(text="Project ID is required")
            return []

        metadata = tracker.latest_message.get("metadata", {})
        cookies = metadata.get("cookies")
        xcsrf_token = metadata.get("X-Csrf-Token")
        
        get_product_details_url = f"{DOMAIN}/service/system/service/serviceCall"

        payload = {
            "serviceCallRequest": {
                "request": [
                    {
                        "service": "catalog.plm.searchProjectItems",
                        "input": {
                            "projectId": project_id,
                            "catalogName": "B2CCatalog",
                            "index": project_id,
                            "category": "PRICE",
                            "itemType": "PRICE",
                            "filter": [
                                {
                                    "name": "productCode",
                                    "value": product_id
                                }
                            ],
                            "__metadata": {
                                "type": "com.kloudville.catalog.plm.component.itemSearchRequest"
                            }
                        },
                        "__metadata": {
                            "type": "com.kloudville.system.services.serviceRequest"
                        }
                    },
                    {
                        "service": "catalog.plm.getInheritedItems",
                        "input": {
                            "projectId": project_id,
                            "itemId": product_id,
                            "itemType": "PRODUCT",
                            "inheritedType": "PRICE",
                            "__metadata": {
                                "type": "com.kloudville.catalog.plm.inheritedItemRequest"
                            }
                        },
                        "__metadata": {
                            "type": "com.kloudville.system.services.serviceRequest"
                        }
                    }
                ],
                "__metadata": {
                    "type": "com.kloudville.system.services.serviceCallRequest"
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
            
            if data is None:
                if language == "ar":
                    dispatcher.utter_message(text="تعذر الوصول إلى تفاصيل المنتج")
                else:
                    dispatcher.utter_message(text="Could not access product details")
                return []
            
            product_items = data.get("serviceCallResult")["result"][0]["output"]["item"]
            formatted_product_items = []
            item_id = product_items[0].get("id")


            # format the product items from KloudVille API
            for product_item in product_items:
                product_name_in_items = [item for item in product_item.get("field") if item["name"] == "productTitle"]
                product_name = product_name_in_items[0].get("displayValue")[0]
                
                product_price_id_in_items = [item for item in product_item.get("field") if item["name"] == "priceId"]
                product_price_id = product_price_id_in_items[0].get("displayValue")[0]

                product_price_value_in_items = [item for item in product_item.get("field") if item["name"] == "value"]
                product_price_value = product_price_value_in_items[0].get("displayValue")[0]
                product_price_title = product_item.get("title")
                # only values needed for formatted items are price id, and price value
                formatted_product_items.append({
                    "product_title": product_name,
                    "price_id": product_price_id,
                    "price_value": product_price_value
                })

            product_title = formatted_product_items[0].get("product_title")
            responseText = ""

            # if more than one price items are found, plural vocab is used, else, singular vocab is used
            if len(formatted_product_items) > 1:
                if language == "ar":
                    responseText = "لقد وجدت " + str(len(formatted_product_items)) + " إصدارات سعر لـ" + product_title + ":"
                else:
                    responseText = "I found " + str(len(formatted_product_items)) + " price versions for " + product_title + ":"
            else:
                if language == "ar":
                    responseText = "لقد وجدت إصدار سعر واحد لـ" + product_title + ":"
                else:
                    responseText = "I found a single price version for " + product_title + ":"

            index = 0
            # iterate through the formatted product items and add it to the final response text
            for product_item in formatted_product_items:
                subResponseText = ""
                if index == len(formatted_product_items) - 1 and len(formatted_product_items) > 1:
                    if language == "ar":
                        subResponseText = " و" + product_price_title + " is SAR" + product_item.get("price_value") + "."
                    else:
                        subResponseText = " and " + product_price_title + " is SAR" + product_item.get("price_value") + "."
                elif len(formatted_product_items) == 1:
                    if language == "ar":
                        subResponseText = " " + product_price_title + " is SAR" + product_item.get("price_value") + "."
                    else:
                        subResponseText = " " + product_price_title + "is SAR" + product_item.get("price_value") + "."
                else:
                    if language == "ar":
                        subResponseText = " " + product_item.get("price_id") + " بقيمة $" + product_item.get("price_value") + ","
                    else:
                        subResponseText = " " + product_item.get("price_id") + " of $" + product_item.get("price_value") + ","
                index += 1
                responseText += subResponseText
            
            dispatcher.utter_message(text=responseText)

            return [ SlotSet("item_id", item_id) ]
        except Exception as e:
            print("Error in fetching")
            print(e)
            dispatcher.utter_message(text="Could not access product details. Please try again later.")
            return []
