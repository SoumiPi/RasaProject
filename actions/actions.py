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
            dispatcher.utter_message(text=f"J'ai sélectionné {food_entity} comme votre choix.")
        else:
            dispatcher.utter_message(text="Désolé, je ne comprends pas votre choix.")

        return []


class OrderFoodAction(Action):
    def name(self) -> Text:
        return "action_order_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="D'accord, quelle nourriture voulez-vous?")

        return []


class ConfirmOrderAction(Action):
    def name(self) -> Text:
        return "action_confirm_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_entity = next(tracker.get_latest_entity_values('nourriture'), None)
        if food_entity:
            dispatcher.utter_message(text=f"J'ai commandé {food_entity} pour vous.")
        else:
            dispatcher.utter_message(text="Désolé, je ne comprends votre choix.")

        return []


#Extractin des periode d'interventions

class ConfirmOrderAction(Action):
    def name(self) -> Text:
        return "action_interventions_periode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        periode_entity = next(tracker.get_latest_entity_values('periode'), None)
        if periode_entity:
            if periode_entity == "aujourd'hui":
                dispatcher.utter_message(text=f"Vous intervenez {periode_entity} aux machines y et y et votre interventions consite à .......")

            if periode_entity == "mois":
                dispatcher.utter_message(text=f"Vous devez intervenir ce {periode_entity} niveau des machines y et y et votre interventions consite à .......")

            if periode_entity == "semaine":
                dispatcher.utter_message(text=f"Vous intervenez cette {periode_entity} aux machines y et y et votre interventions consite à .......")

            if periode_entity == "demain":
                dispatcher.utter_message(text=f" {periode_entity}, vous intervenez aux machines y et y et votre interventions consite à .......")

        else:
            dispatcher.utter_message(text="Désolé, je n'arrive pas à extraire la période d'intervention.")

        return []



class ConfirmOrderAction(Action):
    def name(self) -> Text:
        return "action_interventions_priorite"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        priority_entity = next(tracker.get_latest_entity_values('priorite'), None)
        if priority_entity:
            if priority_entity == "urgemment":
                dispatcher.utter_message(text=f"Vous intervenez {priority_entity} aux machines y et votre interventions consite à .......")

            if priority_entity == "urgentes":
                dispatcher.utter_message(text=f"Les interventions {priority_entity} sont celles  au niveau des machines y")

            if priority_entity == "très urgemment" or "haute priorité" or "les plus urgentes" or "proritaire":
                dispatcher.utter_message(text=f"Vos inteventions les plus urgentes sont aux machines XXX  .......")

        else:
            dispatcher.utter_message(text="Désolé, je n'arrive pas extraire les interventions voulues.")

        return []
