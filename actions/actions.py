
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

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
            if periode_entity == "aujourd'hui":
                dispatcher.utter_message(text=f"Vous intervenez {periode_entity} aux machines y et z et votre interventions consite à .......")

            if periode_entity == "mois":
                dispatcher.utter_message(text=f"Vous devez intervenir ce {periode_entity} niveau des machines y et y et votre interventions consite à .......")

            if periode_entity == "semaine":
                dispatcher.utter_message(text=f"Vous intervenez cette {periode_entity} aux machines y et x et votre interventions consite à .......")

            if periode_entity == "demain":
                dispatcher.utter_message(text=f" {periode_entity}, vous intervenez aux machines y et m1 et votre interventions consite à .......")

        else:
            dispatcher.utter_message(text="Désolé, veuillez préciser la période d'intervention.")

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
        if type_info == "délai de livraison" or "delai de livraison" or "date de livraison" or "livrée":
            response = f"Le délai de livraison pour la demande d'achat numéro {numero_demande} est 12-05-2024."

        elif type_info == "situation":
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


#delai de livraison des bons de commandes

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


#*****************MAGASINIES-*******************************************************************************************************************

#action sur les bons de livraison en retard
class ActionDemanderBonReceptionRetard(Action):

    def name(self) -> Text:
        return "action_demander_bon_reception_retard"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bon_reception_entities = list(tracker.get_latest_entity_values("bon_reception"))
        periode_livraison_entity = next(tracker.get_latest_entity_values("periode_livraison"), None)

        if bon_reception_entities and periode_livraison_entity:
            bon_reception_str = ", ".join(bon_reception_entities)
            periode_livraison_str = periode_livraison_entity
            response = f"Les {bon_reception_str} sont en {periode_livraison_str} sont XYZ."
        else:
            response = "Je suis désolé, je n'ai pas pu trouver toutes les informations nécessaires. Pouvez-vous reformuler votre question ?"

        dispatcher.utter_message(text=response)

        return []


#Action demander la situation de bons de reception
class ActionDemanderStatutBonReception(Action):

    def name(self) -> Text:
        return "action_demander_statut_bon_reception"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bon_reception_entity = next(tracker.get_latest_entity_values("bon_reception"), None)
        numero_bon_reception_entity = next(tracker.get_latest_entity_values("numero_bon_reception"), None)
        type_information_entity = next(tracker.get_latest_entity_values("type_information"), None)

        if bon_reception_entity and numero_bon_reception_entity and type_information_entity:
            response = f"La {type_information_entity} du {bon_reception_entity} numéro {numero_bon_reception_entity} est 'Validée'."
        else:
            response = "Je suis désolé, je n'ai pas pu trouver toutes les informations nécessaires. Pouvez-vous reformuler votre question ?"

        dispatcher.utter_message(text=response)

        return []


#Reondre: savoir les demande de sortie validées
class ActionSavoirDemandeDeSortieValidee(Action):

    def name(self) -> Text:
        return "action_savoir_demande_de_sortie_validee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        demande_sortie_entities = list(tracker.get_latest_entity_values("demande_sortie"))
        situation_entity = next(tracker.get_latest_entity_values("situation"), None)

        if demande_sortie_entities and situation_entity:
            demande_sortie_str = ", ".join(demande_sortie_entities)
            response = f"Les demandes de sortie d'articles dont la situation est {situation_entity} sont les demandes XYZ."
        else:
            response = "Je suis désolé, je n'ai pas pu trouver toutes les informations nécessaires. Pouvez-vous reformuler votre question ?"

        dispatcher.utter_message(text=response)

        return []


#Savoir les bons de commande en retard
class ActionSavoirCommandesRetardLivraison(Action):

    def name(self) -> Text:
        return "action_savoir_commandes_retard_livraison"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # As this is a static response action, we provide a static message.
        dispatcher.utter_message(text="Voici la liste des commandes en retard de livraison: C001, C002, C003.")

        return []




#************************************************************************************************

class ActionEtatEquipementComposantes(Action):

    def name(self) -> Text:
        return "action_etat_equipement_composantes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        etat_equipement = next(tracker.get_latest_entity_values("etat_equipement"), None)

        if etat_equipement:
            response = f"Les équipements en état '{etat_equipement}' sont les suivants: ..."
        else:
            response = "Je n'ai pas pu trouver l'état des équipements demandé. Pouvez-vous reformuler votre question ?"

        dispatcher.utter_message(text=response)
        return []


#connaitre l'historique de transfert equipement
class ActionDemanderHistoriqueTransfertEquipement(Action):

    def name(self) -> Text:
        return "action_demander_historique_transfert_equipement"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        identite_equipement = next(tracker.get_latest_entity_values("identite_equipement"), None)

        if identite_equipement:
            response = f"L'historique de transfert pour l'équipement '{identite_equipement}' est le suivant: ..."
        else:
            response = "Je n'ai pas pu trouver l'identifiant de l'équipement. Pouvez-vous reformuler votre question ?"

        dispatcher.utter_message(text=response)
        return []


#Connaitre la durée des interventions d'un intervenant
class ActionDemanderDureeInterventions(Action):

    def name(self) -> Text:
        return "action_demander_duree_interventions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nom_intervenant = next(tracker.get_latest_entity_values("nom_intervenant"), None)
        mois = next(tracker.get_latest_entity_values("mois"), None)

        if nom_intervenant and mois:
            response = f"La durée des interventions de maintenance pour l'intervenant '{nom_intervenant}' dans le mois de '{mois}' est de X heures."
        else:
            response = "Je n'ai pas pu trouver les informations nécessaires. Pouvez-vous reformuler votre question ?"

        dispatcher.utter_message(text=response)
        return []




#Savoir les demande de sortie à valider ou en attente de validation
class ActionSavoirDemandeDeSortieAValider(Action):

    def name(self) -> Text:
        return "action_savoir_demande_de_sortie_a_valider"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extraction des entités pertinentes
        demande_sortie = next(tracker.get_latest_entity_values("demande_sortie"), None)
        situation = next(tracker.get_latest_entity_values("situation"), None)

        response = "h "

        # Réponse en fonction des entités extraites
        expression_demande_sortie = ["demandes de sortie", "demande de sorties", "demandes de sorties", "demande de sortie", "DS"]
        if demande_sortie and situation:
            if demande_sortie in expression_demande_sortie:
                response = f"Les demandes de sortie d'articles en situation '{situation}' sont les suivantes : ... "
        else:
            response = "Je n'ai pas pu bien comprendre votre requette. Pouvez-vous reformuler votre question ?"

        dispatcher.utter_message(text=response)
        return []




#Savoir les interventions de maintenance préventive plannifiées dans un intervelle de temps à comptyer d'aujourd'hui
class ActionInterventionsMaintenancePreventive(Action):
    def name(self) -> Text:
        return "action_interventions_maintenance_preventive"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        periode_intervention = next(tracker.get_latest_entity_values("periode_intervention"), None)
        type_information = next(tracker.get_latest_entity_values("type_information"), None)

        if periode_intervention and type_information:
            response = f"Les interventions de maintenance préventive prévues pour {periode_intervention} sont {type_information} des equipement X Y Z, etc."
        elif periode_intervention:
            response = f"Il n'y a pas d'informations disponibles pour les interventions de maintenance préventive prévues pour {periode_intervention}."
        else:
            response = "Je suis désolé, je n'ai pas compris votre demande. Pouvez-vous reformuler votre question ?"

        dispatcher.utter_message(text=response)
        return []