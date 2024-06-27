from connect_db import connect_db
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from connexion_db import create_connection



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
                        dispatcher.utter_message(template="utter_periode_non_reconnue")
                        return []

                    # Exécution de la requête SQL
                    cursor.execute(sql_query)
                    work_requests = cursor.fetchall()

                    if work_requests:
                        # Construction du message HTML pour afficher le tableau
                        message += """
                        <table border="1">
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



# class RepondrePeriodeIntervention(Action):
#     def name(self) -> Text:
#         return "action_identifier_interventions"


#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         try:
#             # Connexion à la base de données
#             conn = connect_db()

#             if conn:
#                 cursor = conn.cursor()

#                 # Extraction de l'entité 'periode' depuis le tracker
#                 periode_entity = next(tracker.get_latest_entity_values('periode'), None)

#                 if periode_entity:
#                     if periode_entity == "aujourd'hui":
#                         sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE date_debut_souhaitee = CURDATE()"
#                         message = "<h3>Interventions d'aujourd'hui</h3>"

#                     elif periode_entity == "ce mois":
#                         sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE MONTH(date_debut_souhaitee) = MONTH(CURDATE())"
#                         message = "<h3>Interventions de ce mois-ci</h3>"

#                     elif periode_entity == "cette semaine":
#                         sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE YEARWEEK(date_debut_souhaitee, 1) = YEARWEEK(CURDATE(), 1)"
#                         message = "<h3>Interventions de cette semaine</h3>"

#                     elif periode_entity == "demain":
#                         sql_query = "SELECT equipements, date_debut_souhaitee FROM demande_intervention WHERE date_debut_souhaitee = DATE_ADD(CURDATE(), INTERVAL 1 DAY)"
#                         message = "<h3>Interventions de demain</h3>"

#                     else:
#                         dispatcher.utter_message(template="utter_periode_non_reconnue")
#                         return []

#                     cursor.execute(sql_query)
#                     interventions = cursor.fetchall()

#                     if interventions:
#                         # Ajout de l'entête du tableau
#                         message += """
#                         <table border="1">
#                             <tr>
#                                 <th>Équipements</th>
#                                 <th>Date de début souhaitée</th>
#                             </tr>
#                         """

#                         # Ajout des lignes du tableau
#                         for intervention in interventions:
#                             equipements = intervention[0]
#                             date_debut_souhaitee = intervention[1]
#                             message += f"""
#                             <tr>
#                                 <td>{equipements}</td>
#                                 <td>{date_debut_souhaitee}</td>
#                             </tr>
#                             """

#                         message += "</table>"
#                         dispatcher.utter_message(text=message)
#                     else:
#                         dispatcher.utter_message(text="Aucune intervention trouvée pour cette période.")

#                 else:
#                     dispatcher.utter_message(template="utter_periode_non_reconnue")

#                 cursor.close()
#                 conn.close()

#             else:
#                 dispatcher.utter_message(text="Problème de connexion à la base de données.")

#         except mysql.connector.Error as e:
#             print(f"Erreur MySQL : {e}")
#             dispatcher.utter_message(text="Erreur MySQL lors de la récupération des informations depuis la base de données.")

#         except Exception as e:
#             print(f"Erreur : {e}")
#             dispatcher.utter_message(text="Erreur lors de la récupération des informations depuis la base de données.")

#         return []



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
            dispatcher.utter_message(text = "Erreur MySQL lors de la récupération des informations depuis la base de données.")

        except Exception as e:
            print(f"Erreur : {e}")
            dispatcher.utter_message(text="Erreur lors de la récupération des informations depuis la base de données.")

        return []



# class DebutBonDeTravail(Action):
#     def name(self) -> Text:
#         return "action_debut_bons_de_travail"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         try:
#             # Connexion à la base de données
#             conn = connect_db()

#             if conn:
#                 print("Connexion à la base de données réussie")
#                 cursor = conn.cursor()

#                 # Extraction de l'entité 'date_debut_BT' depuis le tracker
#                 periode_entity = next(tracker.get_latest_entity_values('date_debut_BT'), None)
#                 print(f"Période extraite : {periode_entity}")  # Ajout de logs pour débogage

#                 if periode_entity:
#                     if periode_entity == "aujourd'hui":
#                         sql_query = "SELECT * FROM bon_travail WHERE DATE(date_debut_souhaitee) = CURDATE()"
#                         message = "Les bons de travail qui doivent démarrer aujourd'hui sont les suivants :\n"

#                     elif periode_entity == "mois":
#                         sql_query = "SELECT * FROM bon_travail WHERE MONTH(date_debut_souhaitee) = MONTH(CURDATE())"
#                         message = "Les bons de travail qui doivent démarrer ce mois-ci sont les suivants :\n"

#                     elif periode_entity == "semaine":
#                         sql_query = "SELECT * FROM bon_travail WHERE YEARWEEK(date_debut_souhaitee, 1) = YEARWEEK(CURDATE(), 1)"
#                         message = "Les bons de travail qui doivent démarrer cette semaine sont les suivants :\n"

#                     elif periode_entity == "demain":
#                         sql_query = "SELECT * FROM bon_travail WHERE DATE(date_debut_souhaitee) = DATE_ADD(CURDATE(), INTERVAL 1 DAY)"
#                         message = "Les bons de travail qui doivent démarrer demain sont les suivants :\n"

#                     else:
#                         dispatcher.utter_message(text="Désolé, veuillez préciser la période des bons de travail.")
#                         return []

#                     cursor.execute(sql_query)
#                     bons_travail = cursor.fetchall()

#                     if bons_travail:
#                         response = ""
#                         for bon in bons_travail:
#                             id, numero_activite, numero_bt, categorie, equipement, centre_cout, intervenant, date_debut_souhaitee = bon
#                             response += f"ID: {id}, Numéro d'activité: {numero_activite}, Numéro BT: {numero_bt}, Catégorie: {categorie}, Équipement: {equipement}, Centre de coût: {centre_cout}, Intervenant: {intervenant}, Date début souhaitée: {date_debut_souhaitee}\n"
#                         dispatcher.utter_message(text=message + response)
#                     else:
#                         dispatcher.utter_message(text="Aucun bon de travail trouvé pour la période spécifiée.")

#                 else:
#                     dispatcher.utter_message(text="Désolé, je n'ai pas compris la période spécifiée.")

#                 cursor.close()
#                 conn.close()

#             else:
#                 dispatcher.utter_message(text="Problème de connexion à la base de données.")

#         except mysql.connector.Error as e:
#             print(f"Erreur MySQL : {e}")
#             dispatcher.utter_message(text="Erreur MySQL lors de la récupération des informations depuis la base de données.")

#         except Exception as e:
#             print(f"Erreur : {e}")
#             dispatcher.utter_message(text="Erreur lors de la récupération des informations depuis la base de données.")

#         return []




class RepondrePeriodeIntervention(Action):
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

                    elif periode_entity == "mois":
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

                    elif periode_entity == "semaine":
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

