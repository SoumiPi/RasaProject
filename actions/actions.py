from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ExtractFoodEntity(Action):

    def name(self) -> Text:
         return "action_extract_food_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_entity = next(tracker.get_latest_entity_values('nourriture'), None)
        if food_entity:
            dispatcher.utter_message(text=f" J'ai selectioné {food_entity} comme votre choix ")
        else:
            dispatcher.utter_message(text=f"Désolé, je ne comprends votre choix")

        return []

class OrderFoodAction(Action):
    def name(self) -> Text:
        return "action_order_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        dispatcher.utter_message(text = "D'accord, quelle nourriture voulez-vous? ")

        return []


# class AksFoodPrice(Action):
#     def name(self) -> Text:
#         return "ask_food_price"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         price_entity = next(tracker.get_latest_entitu_values)
#         dispatcher.utter_message(text = "D'accord, quelle nourriture voulez-vous? ")

#         return []

class ConfrimOrderAction(Action):
    def name(self) -> Text:
        return "action_confirm_order"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_entity = next(tracker.get_latest_entity_values('nourriture'), None)
        if food_entity:
            dispatcher.utter_message(text=f"J'ai commandé {food_entity} pour vous")
        else:
            dispatcher.utter_message(text=f"Désolé, je ne comprend pas le choix de la nourriture que vous avez fait")

        return []

