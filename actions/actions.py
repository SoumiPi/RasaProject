
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List



# Classe qui permet d'extraire les entité qui sont les priorité d'intervention

class BonTravailRetard(Action):
    def name(self) -> Text:
        return "action_bons_de_travail_retard"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Les bons de travail en retard sont ............")

        return []




#delai de livraison des bons de commandes

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


#Repondre: savoir les demande de sortie validées
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

        nom_intervenant = tracker.get_slot("nom_intervenant")
        mois = next(tracker.get_latest_entity_values("mois_inte"), None)

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

        # Réponse en fonction des entités extraites
        expression_demande_sortie = ["demandes de sortie", "demande de sorties", "demandes de sorties", "demande de sortie", "DS"]
        if demande_sortie and situation:
            if demande_sortie in expression_demande_sortie:
                dispatcher.utter_message(text = f"Les demandes de sortie d'articles en situation '{situation}' sont les suivantes : ... ")
        else:
            dispatcher.utter_message(text = "Je n'ai pas pu bien comprendre votre requette. Pouvez-vous reformuler votre question ?")

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



#reaprovisionnement

class ActionDemanderReaprovisionnementArticle(Action):

    def name(self) -> Text:
        return "action_demander_reaprovisionnement_article"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extraction des entités 'article' et 'type_information'
        article_entite = next(tracker.get_latest_entity_values("article"), None)
        type_information_entite = next(tracker.get_latest_entity_values("type_information"), None)


        dictionnaire_type_information_entite = ["réapprovisionnés", "réapprovisionnement", "réapprovisionner", "reapprovisionnement", "reapprovisionnés", "reapprovisionné"]
        dictionnaire_article = ["articles", "produits", "artciles"]
        # Logique de réponse basée sur les entités extraites
        if article_entite and type_information_entite:
            if (type_information_entite in dictionnaire_type_information_entite) and (article_entite in  dictionnaire_article):
                dispatcher.utter_message( text= f"Les '{article_entite}' qui ont besoin d'être réapprovisionnés sont les artciles A1, A2, etc'.")

            else:
                dispatcher.utter_message(text = "Je n'ai pas bien compris votre demande. reprenez s'il vous plaît avec les mots clés")

        else:
            dispatcher.utter_message(text = "Je n'ai pas pu bien comprendre votre requette. Pouvez-vous reformuler votre demande ?")

        return []







class ActionDemanderActiviteAvecOuSansBonMoisSemaine(Action):
    def name(self) -> Text:
        return "action_demander_activite_mois_semaine"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extraction de la période d'activité (semaine ou mois) à partir des entités
        periode_activite = next(tracker.get_latest_entity_values("période_activité"), None)
        activite = next(tracker.get_latest_entity_values("activité"), None)

        # Vérification si aucune entité n'a été trouvée
        if not periode_activite or not activite:
            dispatcher.utter_message(text="Veuillez bien préciser s'il s'agit d'une activité avec ou sans bon, ou vérifier la période choisie : les périodes prises en charge sont 'ce mois' et 'cette semaine'.")
            return []

        # Initialisation du message de réponse par défaut
        message = "Je n'ai pas compris la période ou le type d'activité pour laquelle vous voulez des informations."

        # Réponses statiques pour les différentes combinaisons de période et type d'activité
        if periode_activite == "cette semaine":
            if activite == "activités sans bon":
                message = "Voici les activités sans bon prévues pour cette semaine : Activité 1, Activité 2, Activité 3."

            elif activite == "activités":
                message = "Voici les activités prévues pour cette semaine : Activité 1, Activité 2, Activité 3."

        elif periode_activite == "ce mois":
            if activite == "activités sans bon":
                message = "Voici les activités sans bon prévues pour ce mois : Activité A, Activité B, Activité C."

            elif activite == "activités":
                message = "Voici les activités prévues pour ce mois : Activité A, Activité B, Activité C."

        # Envoi du message au dispatcher
        dispatcher.utter_message(text=message)
        return []