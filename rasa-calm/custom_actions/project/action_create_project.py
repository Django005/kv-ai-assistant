import requests
import os

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import datetime

DOMAIN = os.getenv("DOMAIN")

class ActionCreateProject(Action):
    def name(self) -> Text:
        return "action_create_project"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:

        #get language from metadata
        metadata = tracker.latest_message.get("metadata", {})
        language = metadata.get("language")

        project_name = tracker.get_slot("project_name")
        if not project_name:
            dispatcher.utter_message(text="Project Name is required")
            return []

        metadata = tracker.latest_message.get("metadata", {})
        cookies = metadata.get("cookies")
        xcsrf_token = metadata.get("X-Csrf-Token")
        
        # Construct the full URL using DOMAIN from environment variables
        create_project_url = f"{DOMAIN}/service/catalog/plm/createProject"

        headers = {
            "Cookie": cookies,
            "X-Csrf-Token": xcsrf_token
        }

        create_project_payload = {
            "projectCreateRequest": {
                "project": {
                    "projectType": "B2CModifyPOShort",
                    "$projectType": "Shortflow Modify PO",
                    "projectName": project_name,
                    "catalogType": "PRODUCT",
                    "catalog": "B2CCatalog",
                    "ownerId": "Business:demo.user",
                    "sponsorId": "Business:demo.user",
                    "sponsor": {
                        "contactMediumDisplay": "kloudville.demo@gmail.com",
                        "partyRoleType": "INDIVIDUAL",
                        "partyRoleId": "b935f0e8-1196-45e7-b10e-280096dcd6b0",
                        "partyName": "Demo User",
                        "contactMediumId": "d8de62c7-5a6b-4859-9be3-00cdff8bfe62",
                        "contactMediumType": "EMAIL",
                        "source": "MYCOMPANY",
                        "type": "STAFF",
                        "ownerModel": "PLM",
                        "__metadata": {
                            "type": "com.kloudville.party.model.partyRoleInfo",
                            "displayName": "Demo User"
                        }
                    },
                    "owner": {
                        "contactMediumDisplay": "kloudville.demo@gmail.com",
                        "partyRoleType": "INDIVIDUAL",
                        "partyRoleId": "b935f0e8-1196-45e7-b10e-280096dcd6b0",
                        "partyName": "Demo User",
                        "contactMediumId": "d8de62c7-5a6b-4859-9be3-00cdff8bfe62",
                        "contactMediumType": "EMAIL",
                        "source": "MYCOMPANY",
                        "type": "STAFF",
                        "ownerModel": "PLM",
                        "__metadata": {
                            "type": "com.kloudville.party.model.partyRoleInfo",
                            "displayName": "Demo User"
                        }
                    },
                    "__metadata": {
                        "type": "com.kloudville.catalog.plm.model.project",
                        "action": [
                            "Add Attachment",
                            "Add Comment",
                            "runJavaScriptButton",
                            "Download Document",
                            "getTemplates",
                            "createSMSNotification",
                            "refreshErrorHandlingForm",
                            "refreshPAYGDetails",
                            "refreshForm",
                            "refreshPublishingList"
                        ],
                        "displayName": ":",
                        "access": {
                            "projectId": "HIDDEN",
                            "processId": "HIDDEN",
                            "topicId": "HIDDEN",
                            "hasTask": "HIDDEN",
                            "catalog": "HIDDEN",
                            "_default": "READWRITE"
                        }
                    }
                }
            }
        } 

        try:
            response = requests.post(url=create_project_url, json=create_project_payload, headers=headers)
            data = response.json()
            project_id = data.get("project").get("projectId")   
            if language == "ar":
                dispatcher.utter_message(text="تم إنشاء المشروع! معرف المشروع: " + project_id)
            else:
                dispatcher.utter_message(text="Your project has been created! Project ID: " + project_id)
            return [SlotSet("project_id", project_id)]
        except Exception as e:
            dispatcher.utter_message(text="An error occured while creating the project.")