from connect_db import connect_db
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

class RepondrePeriodeIntervention(Action):
    def name(self) -> Text:
        return "action_identifier_interventions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Connexion à la base de données
            conn = connect_db()

            if conn:
                cursor = conn.cursor()

                # Extraction de l'entité 'periode' depuis le tracker
                periode_entity = next(tracker.get_latest_entity_values('periode'), None)

                if periode_entity:
                    if periode_entity == "aujourd'hui":
                        sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE date_debut_souhaitee = CURDATE()"
                        message = f"Vous intervenez aujourd'hui sur les équipements suivants :\n"

                    elif periode_entity == "ce mois":
                        sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE MONTH(date_debut_souhaitee) = MONTH(CURDATE())"
                        message = f"Vous devez intervenir ce mois-ci sur les équipements suivants :\n"

                    elif periode_entity == "cette semaine":
                        sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE YEARWEEK(date_debut_souhaitee, 1) = YEARWEEK(CURDATE(), 1)"
                        message = f"Vous intervenez cette semaine sur les équipements suivants :\n"

                    elif periode_entity == "demain":
                        sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE date_debut_souhaitee = DATE_ADD(CURDATE(), INTERVAL 1 DAY)"
                        message = f"Vous intervenez demain sur les équipements suivants :\n"

                    else:
                        dispatcher.utter_message(template="utter_periode_non_reconnue")
                        return []

                    cursor.execute(sql_query)
                    interventions = cursor.fetchall()

                    if interventions:
                        for intervention in interventions:
                            equipements = intervention[0]
                            date_debut_souhaitee = intervention[1]

                            message += f"- Equipements : {equipements}, Date de début souhaitée : {date_debut_souhaitee}\n"

                        dispatcher.utter_message(text=message)

                    else:
                        dispatcher.utter_message(text="Aucune intervention trouvée pour cette période.")

                else:
                    dispatcher.utter_message(template="utter_periode_non_reconnue")

                cursor.close()
                conn.close()

            else:
                dispatcher.utter_message(text="Problème de connexion à la base de données.")

        except mysql.connector.Error as e:
            print(f"Erreur MySQL : {e}")
            dispatcher.utter_message(text="Erreur MySQL lors de la récupération des informations depuis la base de données.")

        except Exception as e:
            print(f"Erreur : {e}")
            dispatcher.utter_message(text="Erreur lors de la récupération des informations depuis la base de données.")

        return []


class RepondrePrioriteIntervention(Action):
    def name(self) -> Text:
        return "action_identifier_interventions_priorite"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Connexion à la base de données
            conn = connect_db()

            if conn:
                cursor = conn.cursor()

                # Extraction de l'entité 'priorite' depuis le tracker
                priorite_entity = next(tracker.get_latest_entity_values('priorite'), None)

                if priorite_entity:
                    if priorite_entity == "très urgente" or "très urgentes":
                        sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE priorite = 'très urgente'"
                        message = "Les interventions de très haute priorité sont les suivantes :\n"

                    elif priorite_entity == "urgente" or "urgentes":
                        sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE priorite = 'urgente'"
                        message = "Les interventions urgentes sont les suivantes :\n"

                    elif priorite_entity == "moyenne" or "moyennes":
                        sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE priorite = 'moyenne'"
                        message = "Les interventions de priorité moyenne sont les suivantes :\n"

                    else:
                        dispatcher.utter_message(text="Désolé, veuillez spécifier une priorité valide (très urgente, urgente, moyenne).")
                        return []

                    cursor.execute(sql_query)
                    interventions = cursor.fetchall()

                    if interventions:
                        for intervention in interventions:
                            equipements = intervention[0]
                            date_debut_souhaitee = intervention[1]
                            message += f"- Equipements : {equipements}, Date de début souhaitée : {date_debut_souhaitee}\n"

                        dispatcher.utter_message(text=message)
                    else:
                        dispatcher.utter_message(text=f"Aucune intervention trouvée pour la priorité {priorite_entity}.")

                else:
                    dispatcher.utter_message(text="Désolé, je n'ai pas compris la priorité spécifiée.")

                cursor.close()
                conn.close()

            else:
                dispatcher.utter_message(text="Problème de connexion à la base de données.")

        except mysql.connector.Error as e:
            print(f"Erreur MySQL : {e}")
            dispatcher.utter_message(text="Erreur MySQL lors de la récupération des informations depuis la base de données.")

        except Exception as e:
            print(f"Erreur : {e}")
            dispatcher.utter_message(text="Erreur lors de la récupération des informations depuis la base de données.")

        return []



class DebutBonDeTravail(Action):
    def name(self) -> Text:
        return "action_debut_bons_de_travail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Connexion à la base de données
            conn = connect_db()

            if conn:
                print("Connexion à la base de données réussie")
                cursor = conn.cursor()

                # Extraction de l'entité 'date_debut_BT' depuis le tracker
                periode_entity = next(tracker.get_latest_entity_values('date_debut_BT'), None)
                print(f"Période extraite : {periode_entity}")  # Ajout de logs pour débogage

                if periode_entity:
                    if periode_entity == "aujourd'hui":
                        sql_query = "SELECT * FROM bon_travail WHERE DATE(date_debut_souhaitee) = CURDATE()"
                        message = "Les bons de travail qui doivent démarrer aujourd'hui sont les suivants :\n"

                    elif periode_entity == "mois":
                        sql_query = "SELECT * FROM bon_travail WHERE MONTH(date_debut_souhaitee) = MONTH(CURDATE())"
                        message = "Les bons de travail qui doivent démarrer ce mois-ci sont les suivants :\n"

                    elif periode_entity == "semaine":
                        sql_query = "SELECT * FROM bon_travail WHERE YEARWEEK(date_debut_souhaitee, 1) = YEARWEEK(CURDATE(), 1)"
                        message = "Les bons de travail qui doivent démarrer cette semaine sont les suivants :\n"

                    elif periode_entity == "demain":
                        sql_query = "SELECT * FROM bon_travail WHERE DATE(date_debut_souhaitee) = DATE_ADD(CURDATE(), INTERVAL 1 DAY)"
                        message = "Les bons de travail qui doivent démarrer demain sont les suivants :\n"

                    else:
                        dispatcher.utter_message(text="Désolé, veuillez préciser la période des bons de travail.")
                        return []

                    cursor.execute(sql_query)
                    bons_travail = cursor.fetchall()

                    if bons_travail:
                        response = ""
                        for bon in bons_travail:
                            id, numero_activite, numero_bt, categorie, equipement, centre_cout, intervenant, date_debut_souhaitee = bon
                            response += f"ID: {id}, Numéro d'activité: {numero_activite}, Numéro BT: {numero_bt}, Catégorie: {categorie}, Équipement: {equipement}, Centre de coût: {centre_cout}, Intervenant: {intervenant}, Date début souhaitée: {date_debut_souhaitee}\n"
                        dispatcher.utter_message(text=message + response)
                    else:
                        dispatcher.utter_message(text="Aucun bon de travail trouvé pour la période spécifiée.")

                else:
                    dispatcher.utter_message(text="Désolé, je n'ai pas compris la période spécifiée.")

                cursor.close()
                conn.close()

            else:
                dispatcher.utter_message(text="Problème de connexion à la base de données.")

        except mysql.connector.Error as e:
            print(f"Erreur MySQL : {e}")
            dispatcher.utter_message(text="Erreur MySQL lors de la récupération des informations depuis la base de données.")

        except Exception as e:
            print(f"Erreur : {e}")
            dispatcher.utter_message(text="Erreur lors de la récupération des informations depuis la base de données.")

        return []
