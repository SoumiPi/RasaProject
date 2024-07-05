from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from connexion_db import create_connection
from mysql.connector import connect, Error



class RepondrePeriodeIntervention(Action):
    def name(self) -> Text:
        return "action_identifier_interventions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

                # Extraction de l'entité 'periode' depuis le tracker
                periode_entity = next(tracker.get_latest_entity_values('periode'), None)

                if periode_entity:
                    if periode_entity == "aujourd'hui":
                        sql_query = """
                        SELECT
                            wr.work_request_number,
                            wr.work_request_wished_begin_date,
                            p.priority_designation,
                            cc.cost_center_designation,
                            e.equip_designation,
                            wr.work_request_remarks
                        FROM
                            work_request wr
                        LEFT JOIN
                            priority p ON wr.work_request_priority_id = p.priority_id
                        LEFT JOIN
                            cost_center cc ON wr.work_request_cost_center_id = cc.cost_center_id
                        LEFT JOIN
                            equipment e ON wr.work_request_equipment_id = e.equip_id
                        WHERE
                            wr.work_request_wished_begin_date = CURDATE()
                        """
                        message = "<h3>Demandes d'intervention pour aujourd'hui</h3>"

                    elif periode_entity == "ce mois":
                        sql_query = """
                        SELECT
                            wr.work_request_number,
                            wr.work_request_wished_begin_date,
                            p.priority_designation,
                            cc.cost_center_designation,
                            e.equip_designation,
                            wr.work_request_remarks
                        FROM
                            work_request wr
                        LEFT JOIN
                            priority p ON wr.work_request_priority_id = p.priority_id
                        LEFT JOIN
                            cost_center cc ON wr.work_request_cost_center_id = cc.cost_center_id
                        LEFT JOIN
                            equipment e ON wr.work_request_equipment_id = e.equip_id
                        WHERE
                            MONTH(wr.work_request_wished_begin_date) = MONTH(CURDATE())
                        """
                        message = "<h3>Demandes d'intervention pour ce mois-ci</h3>"

                    elif periode_entity == "cette semaine":
                        sql_query = """
                        SELECT
                            wr.work_request_number,
                            wr.work_request_wished_begin_date,
                            p.priority_designation,
                            cc.cost_center_designation,
                            e.equip_designation,
                            wr.work_request_remarks
                        FROM
                            work_request wr
                        LEFT JOIN
                            priority p ON wr.work_request_priority_id = p.priority_id
                        LEFT JOIN
                            cost_center cc ON wr.work_request_cost_center_id = cc.cost_center_id
                        LEFT JOIN
                            equipment e ON wr.work_request_equipment_id = e.equip_id
                        WHERE
                            YEARWEEK(wr.work_request_wished_begin_date, 1) = YEARWEEK(CURDATE(), 1)
                        """
                        message = "<h3>Demandes d'intervention pour cette semaine</h3>"

                    elif periode_entity == "demain":
                        sql_query = """
                        SELECT
                            wr.work_request_number,
                            wr.work_request_wished_begin_date,
                            p.priority_designation,
                            cc.cost_center_designation,
                            e.equip_designation,
                            wr.work_request_remarks
                        FROM
                            work_request wr
                        LEFT JOIN
                            priority p ON wr.work_request_priority_id = p.priority_id
                        LEFT JOIN
                            cost_center cc ON wr.work_request_cost_center_id = cc.cost_center_id
                        LEFT JOIN
                            equipment e ON wr.work_request_equipment_id = e.equip_id
                        WHERE
                            wr.work_request_wished_begin_date = DATE_ADD(CURDATE(), INTERVAL 1 DAY)
                        """
                        message = "<h3>Demandes d'intervention pour demain</h3>"

                    else:
                        dispatcher.utter_message(text="La période que vous avez mentionnée n'est pas encore prise en charge ou est mal écrite")
                        return []

                    # Exécution de la requête SQL
                    cursor.execute(sql_query)
                    work_requests = cursor.fetchall()

                    if work_requests:
                        # Lecture du fichier CSS
                        # with open('style.css', 'r') as file:
                        #     css = file.read()

                        # Construction du message HTML pour afficher le tableau
                        message += f"""
                        <style>
                        h3 {{
                            font-size: 18px;
                        }}
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                        }}
                        th, td {{
                            border: 1px solid black;
                            padding: 8px;
                            text-align: left;
                        }}
                        th {{
                            background-color: white;
                            color: navy;
                        }}
                        </style>
                        <table>
                            <tr>
                                <th>Numéro de demande</th>
                                <th>Date de début souhaitée</th>
                                <th>Priorité</th>
                                <th>Centre de coût</th>
                                <th>Équipement</th>
                                <th>Remarques</th>
                            </tr>
                        """
                        for wr in work_requests:
                            work_request_number = wr[0]
                            work_request_wished_begin_date = wr[1]
                            priority_designation = wr[2]
                            cost_center_designation = wr[3]
                            equip_designation = wr[4]
                            work_request_remarks = wr[5]

                            message += f"""
                            <tr>
                                <td>{work_request_number}</td>
                                <td>{work_request_wished_begin_date}</td>
                                <td>{priority_designation}</td>
                                <td>{cost_center_designation}</td>
                                <td>{equip_designation}</td>
                                <td>{work_request_remarks}</td>
                            </tr>
                            """
                        message += "</table>"
                        dispatcher.utter_message(text=message)

                    else:
                        dispatcher.utter_message(text=f"Aucune demande d'intervention trouvée pour la période {periode_entity}.")

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

class RepondreInterventionsUrgentes(Action):
    def name(self) -> Text:
        return "action_identifier_interventions_priorite"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

                # Extraction des entités 'priorite' et 'priority_periode' depuis le tracker
                priorite_entity = next(tracker.get_latest_entity_values('priorite'), None)
                priority_periode_entity = next(tracker.get_latest_entity_values('priority_periode'), None)

                if priorite_entity and priority_periode_entity:
                    periode_condition = ""
                    if priority_periode_entity == "aujourd'hui":
                        periode_condition = "wr.work_request_wished_begin_date = CURDATE()"
                    elif priority_periode_entity in ["ce mois", "ce mois-ci"]:
                        periode_condition = "MONTH(wr.work_request_wished_begin_date) = MONTH(CURDATE())"
                    elif priority_periode_entity == "cette semaine":
                        periode_condition = "YEARWEEK(wr.work_request_wished_begin_date, 1) = YEARWEEK(CURDATE(), 1)"
                    elif priority_periode_entity == "semaine prochaine":
                        periode_condition = "YEARWEEK(wr.work_request_wished_begin_date, 1) = YEARWEEK(DATE_ADD(CURDATE(), INTERVAL 1 WEEK), 1)"
                    elif priority_periode_entity == "mois prochain":
                        periode_condition = "MONTH(wr.work_request_wished_begin_date) = MONTH(DATE_ADD(CURDATE(), INTERVAL 1 MONTH))"
                    else:
                        dispatcher.utter_message(text=f"La période '{priority_periode_entity}' n'est pas reconnue. Les périodes reconnues sont: 'ce moisc mois prochain, cette semaine, semaine prochaine'")
                        return []

                    priority_condition = ""
                    if priorite_entity in ["très urgentes","très urgente"]:
                        priority_condition = "p.priority_id = 1"
                    elif priorite_entity in ["urgentes", "urgente"]:
                        priority_condition = "p.priority_id = 2"
                    else:
                        dispatcher.utter_message(text=f"La priorité '{priorite_entity}' n'est pas reconnue. Les prorités reconnues sont 'urgentes, très urgentes'.")
                        return []

                    # Requête SQL pour récupérer les interventions prioritaires
                    sql_query = f"""
                        SELECT
                            wr.work_request_number,
                            wr.work_request_wished_begin_date,
                            p.priority_designation,
                            cc.cost_center_designation,
                            e.equip_designation,
                            wr.work_request_remarks
                        FROM
                            work_request wr
                        LEFT JOIN
                            priority p ON wr.work_request_priority_id = p.priority_id
                        LEFT JOIN
                            cost_center cc ON wr.work_request_cost_center_id = cc.cost_center_id
                        LEFT JOIN
                            equipment e ON wr.work_request_equipment_id = e.equip_id
                        WHERE
                            {priority_condition}
                            AND {periode_condition}
                        """
                    message = f"""
                    <style>
                        h3 {{
                            font-size: 18px;
                        }}
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                        }}
                        th, td {{
                            border: 1px solid black;
                            padding: 8px;
                            text-align: left;
                        }}
                        th {{
                            background-color: white;
                            color: navy;
                        }}
                    </style>
                    <h3>Demandes d'intervention {priorite_entity} pour '{priority_periode_entity}'</h3>
                    <table>
                        <tr>
                            <th>Numéro de demande</th>
                            <th>Date de début souhaitée</th>
                            <th>Priorité</th>
                            <th>Centre de coût</th>
                            <th>Équipement</th>
                            <th>Remarques</th>
                        </tr>
                    """

                    # Exécution de la requête SQL
                    cursor.execute(sql_query)
                    interventions = cursor.fetchall()

                    if interventions:
                        for wr in interventions:
                            work_request_number = wr[0]
                            work_request_wished_begin_date = wr[1]
                            priority_designation = wr[2]
                            cost_center_designation = wr[3]
                            equip_designation = wr[4]
                            work_request_remarks = wr[5]

                            message += f"""
                            <tr>
                                <td>{work_request_number}</td>
                                <td>{work_request_wished_begin_date}</td>
                                <td>{priority_designation}</td>
                                <td>{cost_center_designation}</td>
                                <td>{equip_designation}</td>
                                <td>{work_request_remarks}</td>
                            </tr>
                            """
                        message += "</table>"
                        dispatcher.utter_message(text=message, parse_mode="HTML")

                    else:
                        dispatcher.utter_message(text=f"Il n'y a pas de demande d'intervention {priorite_entity} trouvées pour '{priority_periode_entity}'.")

                else:
                    dispatcher.utter_message(text="Les informations nécessaires pour la requête sont incomplètes ou incorrectes.")

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

class RepondreDebutBonTravail(Action):
    def name(self) -> Text:
        return "action_debut_bons_de_travail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

                # Extraction de l'entité 'date_debut_BT' depuis le tracker
                periode_entity = next(tracker.get_latest_entity_values('date_debut_BT'), None)

                if periode_entity:
                    if periode_entity == "aujourd'hui":
                        sql_query = """
                        SELECT
                            wo.work_order_number,
                            e.equip_designation AS equipment_name,
                            cc.cost_center_designation AS cost_center_name,
                            wo.work_order_begin_date,
                            wo.work_order_remarks
                        FROM
                            work_order wo
                        LEFT JOIN
                            equipment e ON wo.work_order_equipment_id = e.equip_id
                        LEFT JOIN
                            cost_center cc ON wo.work_order_cost_center_id = cc.cost_center_id
                        WHERE
                            wo.work_order_begin_date = CURDATE();
                        """
                        message = "<h3>Les bons de travail prévus pour aujourd'hui sont :</h3>"

                    elif periode_entity in ["ce mois", "mois en cours"]:
                        sql_query = """
                        SELECT
                            wo.work_order_number,
                            e.equip_designation AS equipment_name,
                            cc.cost_center_designation AS cost_center_name,
                            wo.work_order_begin_date,
                            wo.work_order_remarks
                        FROM
                            work_order wo
                        LEFT JOIN
                            equipment e ON wo.work_order_equipment_id = e.equip_id
                        LEFT JOIN
                            cost_center cc ON wo.work_order_cost_center_id = cc.cost_center_id
                        WHERE
                            MONTH(wo.work_order_begin_date) = MONTH(CURDATE());
                        """
                        message = "<h3>Les bons de travail prévus pour ce mois sont :</h3>"

                    elif periode_entity in ["cette semaine", "semaine en cours"]:
                        sql_query = """
                        SELECT
                            wo.work_order_number,
                            e.equip_designation AS equipment_name,
                            cc.cost_center_designation AS cost_center_name,
                            wo.work_order_begin_date,
                            wo.work_order_remarks
                        FROM
                            work_order wo
                        LEFT JOIN
                            equipment e ON wo.work_order_equipment_id = e.equip_id
                        LEFT JOIN
                            cost_center cc ON wo.work_order_cost_center_id = cc.cost_center_id
                        WHERE
                            YEARWEEK(wo.work_order_begin_date, 1) = YEARWEEK(CURDATE(), 1);
                        """
                        message = "<h3>Les bons de travail prévus pour cette semaine sont :</h3>"

                    elif periode_entity == "demain":
                        sql_query = """
                        SELECT
                            wo.work_order_number,
                            e.equip_designation AS equipment_name,
                            cc.cost_center_designation AS cost_center_name,
                            wo.work_order_begin_date,
                            wo.work_order_remarks
                        FROM
                            work_order wo
                        LEFT JOIN
                            equipment e ON wo.work_order_equipment_id = e.equip_id
                        LEFT JOIN
                            cost_center cc ON wo.work_order_cost_center_id = cc.cost_center_id
                        WHERE
                            wo.work_order_begin_date = DATE_ADD(CURDATE(), INTERVAL 1 DAY);
                        """
                        message = "<h3>Les bons de travail prévus pour demain sont :</h3>"

                    else:
                        dispatcher.utter_message(response="utter_periode_non_reconnue")
                        return []

                    cursor.execute(sql_query)
                    interventions = cursor.fetchall()

                    if interventions:
                        message += """
                        <table border="1" style="width:100%; border-collapse: collapse;">
                            <tr style="background-color:#f2f2f2;">
                                <th style="padding: 8px; text-align: left;">Numéro de bon</th>
                                <th style="padding: 8px; text-align: left;">Équipement</th>
                                <th style="padding: 8px; text-align: left;">Centre de coût</th>
                                <th style="padding: 8px; text-align: left;">Date de début</th>
                                <th style="padding: 8px; text-align: left;">Remarques</th>
                            </tr>
                        """

                        for intervention in interventions:
                            work_order_number, equipment_name, cost_center_name, work_order_begin_date, work_order_remarks = intervention
                            message += f"""
                            <tr>
                                <td style="padding: 8px; text-align: left;">{work_order_number}</td>
                                <td style="padding: 8px; text-align: left;">{equipment_name}</td>
                                <td style="padding: 8px; text-align: left;">{cost_center_name}</td>
                                <td style="padding: 8px; text-align: left;">{work_order_begin_date}</td>
                                <td style="padding: 8px; text-align: left;">{work_order_remarks}</td>
                            </tr>
                            """

                        message += "</table>"
                        dispatcher.utter_message(text=message, parse_mode="HTML")

                    else:
                        dispatcher.utter_message(text="Aucun bon de travail trouvé pour cette période.")

                else:
                    dispatcher.utter_message(response="utter_periode_non_reconnue")

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

class ActionDemanderTournees(Action):
    def name(self) -> Text:
        return "action_demander_tournees_semaine_mois"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

                # Extraction des entités 'tournee' et 'periode_tournee' depuis le tracker
                tournee_entite = next(tracker.get_latest_entity_values("tournee"), None)
                periode_entite = next(tracker.get_latest_entity_values("periode_tournee"), None)

                dictionnaire_tournee_entite = ["tournées", "tournés", "tournees", "tourné"]

                if tournee_entite and periode_entite and tournee_entite in dictionnaire_tournee_entite:
                    # Définir la condition de la période
                    periode_condition = ""
                    if periode_entite == "aujourd'hui":
                        periode_condition = "campaign.campaign_wished_begin_date = CURDATE()"
                    elif periode_entite in ["ce mois", "mois en cours"]:
                        periode_condition = "MONTH(campaign.campaign_wished_begin_date) = MONTH(CURDATE())"
                    elif periode_entite in ["cette semaine", "semaine en cours"]:
                        periode_condition = "YEARWEEK(campaign.campaign_wished_begin_date, 1) = YEARWEEK(CURDATE(), 1)"
                    elif periode_entite in ["la semaine prochaine", "la semaine suivante"]:
                        periode_condition = "YEARWEEK(campaign.campaign_wished_begin_date, 1) = YEARWEEK(DATE_ADD(CURDATE(), INTERVAL 1 WEEK), 1)"
                    elif periode_entite in ["le mois prochain", "le mois suivant"]:
                        periode_condition = "MONTH(campaign.campaign_wished_begin_date) = MONTH(DATE_ADD(CURDATE(), INTERVAL 1 MONTH))"
                    else:
                        dispatcher.utter_message(text=f"La période '{periode_entite}' n'est pas reconnue pour le moment.")
                        return []

                    # Requête SQL pour récupérer les campagnes
                    sql_query = f"""
                        SELECT
                            campaign.campaign_code,
                            campaign.campaign_designation,
                            cc.cost_center_designation,
                            e.equip_designation,
                            campaign.campaign_wished_begin_date
                        FROM
                            campaign
                        LEFT JOIN
                            cost_center cc ON campaign.campaign_cost_center_id = cc.cost_center_id
                        LEFT JOIN
                            equipment e ON campaign.campaign_equipment_id = e.equip_id
                        WHERE
                            {periode_condition}
                        """

                    # Exécution de la requête SQL
                    cursor.execute(sql_query)
                    tournees = cursor.fetchall()

                    if tournees:
                        message = f"""
                        <style>
                            h3 {{
                                font-size: 18px;
                            }}
                            table {{
                                border-collapse: collapse;
                                width: 100%;
                            }}
                            th, td {{
                                border: 1px solid black;
                                padding: 8px;
                                text-align: left;
                            }}
                            th {{
                                background-color: white;
                                color: navy;
                            }}
                        </style>
                        <h3>Tournées planifiées pour '{periode_entite}'</h3>
                        <table>
                            <tr>
                                <th>Code</th>
                                <th>Désignation</th>
                                <th>Centre de coût</th>
                                <th>Équipement</th>
                                <th>Date souhaitée</th>
                            </tr>
                        """

                        for tournee in tournees:
                            campaign_code = tournee[0]
                            campaign_designation = tournee[1]
                            cost_center_designation = tournee[2]
                            equip_designation = tournee[3]
                            campaign_wished_begin_date = tournee[4]

                            message += f"""
                            <tr>
                                <td>{campaign_code}</td>
                                <td>{campaign_designation}</td>
                                <td>{cost_center_designation}</td>
                                <td>{equip_designation}</td>
                                <td>{campaign_wished_begin_date}</td>
                            </tr>
                            """
                        message += "</table>"
                        dispatcher.utter_message(text=message, parse_mode="HTML")

                    else:
                        dispatcher.utter_message(text=f"Aucune tournée trouvée pour '{periode_entite}'.")

                else:
                    dispatcher.utter_message(text="Les informations nécessaires pour la requête sont incomplètes ou incorrectes.")

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
