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

class RepondrePeriodeIntervention(Action):
    def name(self) -> Text:
        return "action_interventions_periode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        periode_entity = next(tracker.get_latest_entity_values('periode'), None)
        if periode_entity:
            if periode_entity == "aujourd'hui" or "jour":
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


# Classe qui permet d'extraire les entité qui sont les priorité d'intervention
class RepondrePrioriteIntervention(Action):
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

        else:
            dispatcher.utter_message(text="Désolé, je n'arrive pas extraire les interventions voulues.")

        return []


#classe qui permet d'extraire les date de  debut d'excution des bons de travail
class DebutBonDeTravail(Action):
    def name(self) -> Text:
        return "action_debut_bons_de_travail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        Bon_date_entity = next(tracker.get_latest_entity_values('date_debut_BT'), None)
        if Bon_date_entity:
            if Bon_date_entity == "mois":
                dispatcher.utter_message(text=f"Les bons de travail qui commencent ce {Bon_date_entity} sont les bons .......")

            if Bon_date_entity == "aujourd'hui":
                dispatcher.utter_message(text=f"Les bons de travail qui doivent demarrer {Bon_date_entity} sont les suivantes: ...... Il s'agit de ....")

            if Bon_date_entity == "semaine":
                dispatcher.utter_message(text=f"Les bons de travail qui commencent cette  {Bon_date_entity} sont les bons N° 0061 ET N° 0021")

        else:
            dispatcher.utter_message(text="Désolé, je n'arrive pas extraire les dates voulues.")

        return []


class BonTravailRetard(Action):
    def name(self) -> Text:
        return "action_bons_de_travail_retard"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Les bons de travail en retard sont ............")

        return []


#Gestion des demande d'achat: Class qui gerer permettre les demande d'achat, leur founisseur à travers les numéro de commande d'achat
class RepondreDemandeAchat(Action):
    def name(self) -> Text:
        return "action_repondre_demande_achat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        type_info = next(tracker.get_latest_entity_values('type_information'), None)
        numero_demande = next(tracker.get_latest_entity_values('numero_demande'), None)

        if not numero_demande:
            dispatcher.utter_message(text="Désolé, je n'ai pas trouvé le numéro de la demande d'achat. Pouvez-vous préciser ?")
            return []

        # Simulated responses for demonstration purposes
        if type_info == "délai de livraison":
            response = f"Le délai de livraison pour la demande d'achat numéro {numero_demande} est 12-05-2024."

        elif type_info == "statut":
            response = f"Le statut actuel de la demande d'achat numéro {numero_demande} est 'En cours de traitement'."

        elif type_info == "fournisseur":
            response = f"Le fournisseur pour la demande d'achat numéro {numero_demande} est 'SOFIANE'."

        else:
            response = "Je ne suis pas sûr du type d'information que vous demandez. Pouvez-vous préciser si vous voulez le délai de livraison, le statut ou le fournisseur ?"

        dispatcher.utter_message(text=response)

        return []


#Classe de la demande d'achat v
class ActionDemanderSituationDemandeAchatValidee(Action):
    def name(self) -> Text:
        return "action_demander_situation_demande_achat_validee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extraction des entités 'situation' et 'periode_demande'
        situation = next(tracker.get_latest_entity_values('situation'), None)
        periode_demande = next(tracker.get_latest_entity_values('periode_demande'), None)

        # Vérification des entités extraites et génération de la réponse
        if situation and periode_demande:
            response = f"Les demandes d'achat '{situation}' dans la période de :'{periode_demande}' sont les demandes 0061, 0035 , etc."
        else:
            response = "Désolé, je n'ai pas compris la situation ou la période de demande spécifiée."

        dispatcher.utter_message(text=response)

        return []


    #delai de livraison

class ActionBonsCommandeDateLivraison(Action):
    def name(self) -> Text:
        return "action_bons_commande_date_livraison"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extraction des entités 'date_livraison' et 'periode_livraison'
        type_information = next(tracker.get_latest_entity_values('type_information'), None)
        periode_livraison = next(tracker.get_latest_entity_values('periode_livraison'), None)

        # Construction du message de réponse en fonction des entités extraites
        if type_information and periode_livraison:
            response = f"Les commandes qui doivent être livrées '{periode_livraison}' sont les commandes N° ......."


        else:
            response = "Désolé, je n'ai pas compris la date ou la période de livraison spécifiée."

        dispatcher.utter_message(text=response)
        return []