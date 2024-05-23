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


#Creation des acteurs


class ActionRecueillirInfosActeur(Action):
    def name(self) -> Text:
        return "action_recueillir_infos_acteur"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Liste des informations à recueillir
        infos_a_recueillir = ["nom", "prénom", "code", "numéro de téléphone"]

        # Initialiser le dictionnaire pour stocker les informations de l'acteur
        acteur_infos = {}

        # Vérifier chaque information et demander à l'utilisateur si elle manque
        for info in infos_a_recueillir:
            if not tracker.get_slot(info):
                dispatcher.utter_message(text="Pourriez-vous me fournir {} de l'acteur ?".format(info))
                return []

            # Si l'information est fournie, l'ajouter au dictionnaire
            acteur_infos[info] = tracker.get_slot(info)

        # Afficher les informations recueillies avec succès
        dispatcher.utter_message(text="Informations de l'acteur recueillies avec succès:")
        for info, valeur in acteur_infos.items():
            dispatcher.utter_message(text="- {}: {}".format(info.capitalize(), valeur))

        return []
