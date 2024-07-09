#import jwt
from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from connexion_db import create_connection
import mysql
# from get_user_rule_token import get_user_rule_from_token
        # Récupération du token JWT depuis les métadonnées du tracker
        # token = tracker.latest_message.get('metadata', {}).get('token')
        # user_role = get_user_rule_from_token(token)
        # print(f"Rôle de l'utilisateur : {user_role}")

        # # Vérification du rôle pour autoriser l'action
        # if user_role not in ['technicien', 'Magasinier', 'Responsable Achat']:  # Ajoutez les rôles autorisés ici
        #     dispatcher.utter_message(text="Désolé, vous n'avez pas le droit d'accès à ces informations.")
        #     return []


class ActionDemandeAchatFournisseur(Action):
    def name(self) -> Text:
        return "action_demander_fournisseur_demande_achat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = 17 # ID de l'utilisateur pour l'exemple

        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

                # Requête SQL pour récupérer user_profile_id
                sql_query = f"""
                    SELECT up.user_profile_id
                    FROM user u
                    JOIN user_company uc ON u.user_id = uc.user_company_user_id
                    JOIN user_profile up ON uc.user_company_profile_id = up.user_profile_id
                    WHERE u.user_id = {user_id}
                """
                cursor.execute(sql_query)
                row = cursor.fetchone()

                if row:
                    user_profile_id = row[0]

                    # Vérification si l'utilisateur a le bon profil
                    if user_profile_id != 8:
                        dispatcher.utter_message(text="Désolé, votre profil ne vous permet pas d'avoir accès à ces informations")
                        return []
                else:
                    dispatcher.utter_message(text="Utilisateur non trouvé.")
                    return []

                # Extraction des entités depuis le tracker
                numero_demande = next(tracker.get_latest_entity_values('numero_demande'), None)
                demande_achat = next(tracker.get_latest_entity_values('demande_achat'), None)
                type_information = next(tracker.get_latest_entity_values('type_information'), None)

                # Vérification des entités pertinentes
                if demande_achat in ["demandes d'achat", "demande d'achat", "DA"] and type_information in ["fournisseur", "prestataire"]:
                    if numero_demande:
                        # Requête SQL pour récupérer le fournisseur de la demande spécifiée
                        sql_query = f"""
                            SELECT s.supplier_designation
                            FROM purchase_requisition pr
                            LEFT JOIN supplier s ON pr.purchase_requisition_supplier_id = s.supplier_id
                            WHERE pr.purchase_requisition_number = '{numero_demande}'
                        """
                        cursor.execute(sql_query)
                        fournisseur = cursor.fetchone()

                        if fournisseur:
                            supplier_designation = fournisseur[0]
                            response = f"Le fournisseur pour la demande d'achat numéro {numero_demande} est {supplier_designation}."
                            dispatcher.utter_message(text=response)
                        else:
                            dispatcher.utter_message(text=f"Aucune information trouvée pour le fournisseur de la demande d'achat numéro {numero_demande}.")
                    else:
                        dispatcher.utter_message(text="Le numéro de demande spécifié est invalide ou manquant.")
                else:
                    dispatcher.utter_message(text="Je ne comprends pas votre demande, veuillez reformuler votre question.")

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

#pas ok
class ActionDemandeAchatDelaiLivraison(Action):
    def name(self) -> Text:
        return "action_demande_delai_livraison_demande_achat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = 17
        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

                # Requête SQL pour récupérer user_profile_id
                sql_query = f"""
                    SELECT up.user_profile_id
                    FROM user u
                    JOIN user_company uc ON u.user_id = uc.user_company_user_id
                    JOIN user_profile up ON uc.user_company_profile_id = up.user_profile_id
                    WHERE u.user_id = {user_id}
                """
                cursor.execute(sql_query)
                row = cursor.fetchone()

                if row:
                    user_profile_id = row[0]

                    # Vérification si l'utilisateur a le bon profil
                    if user_profile_id != 8:
                        dispatcher.utter_message(text="Désolé, votre profil ne vous permet pas d'avoir accès à ces informations")
                        return []
                # Extraction de l'entité 'numero_demande' depuis le tracker
                numero_demande = next(tracker.get_latest_entity_values('numero_demande'), None)
                type_information = next(tracker.get_latest_entity_values('type_information'), None)
                demande_achat = next(tracker.get_latest_entity_values('demande_achat'), None)


                if numero_demande and type_information and demande_achat:
                    if type_information in ["délai de livraison", "date de livraison"] and demande_achat in ["demande d'achat", "DA", "demandes d'achat"]:
                        # Requête SQL pour récupérer la date de livraison souhaitée pour la demande spécifiée
                        sql_query = f"""
                            SELECT purchase_requisition_delivery_wish_date
                            FROM purchase_requisition
                            WHERE purchase_requisition_number = '{numero_demande}'
                            """

                        # Exécution de la requête SQL
                        cursor.execute(sql_query)
                        demande_achat = cursor.fetchone()

                        if demande_achat:
                            livraison_souhaitee = demande_achat[0]
                            response = f"La date de livraison souhaitée pour la demande d'achat numéro {numero_demande} est prévue pour le {livraison_souhaitee}."
                            dispatcher.utter_message(text=response)
                        else:
                            dispatcher.utter_message(text=f"Aucune information trouvée sur la date de livraison souhaitée de la demande d'achat numéro {numero_demande}.")
                    else:
                        dispatcher.utter_message(text="Type d'information ou demande d'achat invalide.")
                else:
                    dispatcher.utter_message(text="Veuillez spécifier toutes les informations nécessaires : numéro de demande, type d'information et type de demande d'achat.")

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

#ok
class ActionDemandeAchatSituation(Action):
    def name(self) -> Text:
        return "action_demande_situation_demande_achat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = 17

        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

                # Requête SQL pour récupérer user_profile_id
                sql_query = f"""
                    SELECT up.user_profile_id
                    FROM user u
                    JOIN user_company uc ON u.user_id = uc.user_company_user_id
                    JOIN user_profile up ON uc.user_company_profile_id = up.user_profile_id
                    WHERE u.user_id = {user_id}
                """
                cursor.execute(sql_query)
                row = cursor.fetchone()

                if row:
                    user_profile_id = row[0]

                    # Vérification si l'utilisateur a le bon profil
                    if user_profile_id != 8:
                        dispatcher.utter_message(text="Désolé, votre profil ne vous permet pas d'avoir accès à ces informations")
                        return []
                # Extraction de l'entité 'numero_demande' depuis le tracker
                numero_demande = next(tracker.get_latest_entity_values('numero_demande'), None)
                type_information = next(tracker.get_latest_entity_values('type_information'), None)
                demande_achat = next(tracker.get_latest_entity_values('demande_achat'), None)

                if demande_achat and type_information in ["situation", "statut"]:

                    if numero_demande:
                        # Requête SQL pour récupérer la situation de la demande d'achat

                        sql_query = f"""
                            SELECT ps.purchase_situation_french_designation
                            FROM purchase_requisition pr
                            LEFT JOIN purchase_situation ps ON pr.purchase_requisition_situation_id = ps.purchase_situation_id
                            WHERE pr.purchase_requisition_number = '{numero_demande}'
                        """

                        # Exécution de la requête SQL
                        cursor.execute(sql_query)
                        result = cursor.fetchone()

                        if result:
                            situation_description = result[0]
                            dispatcher.utter_message(text=f"La situation de la demande d'achat numéro {numero_demande} est : {situation_description}")
                        else:
                            dispatcher.utter_message(text=f"Aucune information trouvée pour la demande d'achat numéro {numero_demande}.")
                    else:
                        dispatcher.utter_message(text="Le numéro de demande n'est pas spécifié.")

                    # Fermeture du curseur et de la connexion à la base de données
                    cursor.close()
                    conn.close()
                else:
                    dispatcher.utter_message(text="Spécifiez bien 'demandes d'achat'.")



            else:
                dispatcher.utter_message(text="Problème de connexion à la base de données.")

        except Exception as e:
            print(f"Erreur lors de la récupération de la situation de la demande d'achat : {e}")
            dispatcher.utter_message(text="Erreur lors de la récupération de l'information depuis la base de données.")

        return []


class ActionDemandesAchatPeriodeLivraison(Action):
    def name(self) -> Text:
        return "action_demandes_achat_periode_livraison"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = 17


        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

                # Requête SQL pour récupérer user_profile_id
                sql_query = f"""
                    SELECT up.user_profile_id
                    FROM user u
                    JOIN user_company uc ON u.user_id = uc.user_company_user_id
                    JOIN user_profile up ON uc.user_company_profile_id = up.user_profile_id
                    WHERE u.user_id = {user_id}
                """
                cursor.execute(sql_query)
                row = cursor.fetchone()

                if row:
                    user_profile_id = row[0]

                    # Vérification si l'utilisateur a le bon profil
                    if user_profile_id != 8:
                        dispatcher.utter_message(text="Désolé, votre profil ne vous permet pas d'avoir accès à ces informations")
                        return []
                # Extraction des entités 'type_information' et 'periode_livraison' depuis le tracker
                type_information = next(tracker.get_latest_entity_values('demande_achat'), None)
                periode_livraison = next(tracker.get_latest_entity_values('periode_livraison'), None)

                # Construction de la condition de période
                periode_condition = ""
                if periode_livraison and type_information:
                    if periode_livraison in ["cette semaine", "semaine en cours"]:
                        periode_condition = "WEEK(purchase_requisition_delivery_wish_date) = WEEK(CURDATE()) AND YEAR(purchase_requisition_delivery_wish_date) = YEAR(CURDATE())"
                    elif periode_livraison in ["semaine prochaine", "semaine suivante"]:
                        periode_condition = "DATE(purchase_requisition_delivery_wish_date) = CURDATE()"
                    elif periode_livraison in ["mois en cours" , "ce mois"]:
                        periode_condition = "MONTH(purchase_requisition_delivery_wish_date) = MONTH(CURDATE()) AND YEAR(purchase_requisition_delivery_wish_date) = YEAR(CURDATE())"
                    elif periode_livraison in ["mois suivant", "mois prochain"]:
                        periode_condition = "MONTH(purchase_requisition_delivery_wish_date) = MONTH(DATE_ADD(CURDATE(), INTERVAL 1 MONTH)) AND YEAR(purchase_requisition_delivery_wish_date) = YEAR(DATE_ADD(CURDATE(), INTERVAL 1 MONTH))"
                    else:
                        dispatcher.utter_message(text=f"La période '{periode_livraison}' n'est pas reconnue pour le moment.")
                        return []

                    # Requête SQL pour récupérer les demandes d'achat
                    sql_query = f"""
                        SELECT
                            purchase_requisition_number,
                            purchase_requisition_delivery_wish_date,
                            purchase_requisition_buyer,
                            purchase_requisition_requester,
                            cc.cost_center_designation
                        FROM
                            purchase_requisition
                        LEFT JOIN
                            cost_center cc ON purchase_requisition.purchase_requisition_cost_center_id = cc.cost_center_id
                        WHERE
                            {periode_condition}
                        """

                    # Exécution de la requête SQL
                    cursor.execute(sql_query)
                    demandes_achat = cursor.fetchall()

                    if demandes_achat:
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
                        <h3>Demandes d'achat pour '{periode_livraison}'</h3>
                        <table>
                            <tr>
                                <th>Numéro de demande</th>
                                <th>Date de livraison souhaitée</th>
                                <th>Acheteur</th>
                                <th>Demandeur</th>
                                <th>Centre de coût</th>
                            </tr>
                        """

                        for demande in demandes_achat:
                            purchase_requisition_number = demande[0]
                            purchase_requisition_delivery_wish_date = demande[1]
                            purchase_requisition_buyer = demande[2]
                            purchase_requisition_requester = demande[3]
                            cost_center_designation = demande[4]

                            message += f"""
                            <tr>
                                <td>{purchase_requisition_number}</td>
                                <td>{purchase_requisition_delivery_wish_date}</td>
                                <td>{purchase_requisition_buyer}</td>
                                <td>{purchase_requisition_requester}</td>
                                <td>{cost_center_designation}</td>
                            </tr>
                            """
                        message += "</table>"
                        dispatcher.utter_message(text=message, parse_mode="HTML")

                    else:
                        dispatcher.utter_message(text=f"Aucune demande d'achat trouvée pour '{periode_livraison}'.")

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


class ActionBonsCommandePeriodeLivraison(Action):
    def name(self) -> Text:
        return "action_bons_commande_periode_livraison"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = 17

        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()


                # Requête SQL pour récupérer user_profile_id
                sql_query = f"""
                    SELECT up.user_profile_id
                    FROM user u
                    JOIN user_company uc ON u.user_id = uc.user_company_user_id
                    JOIN user_profile up ON uc.user_company_profile_id = up.user_profile_id
                    WHERE u.user_id = {user_id}
                """
                cursor.execute(sql_query)
                row = cursor.fetchone()

                if row:
                    user_profile_id = row[0]

                    # Vérification si l'utilisateur a le bon profil
                    if user_profile_id != 8:
                        dispatcher.utter_message(text="Désolé, votre profil ne vous permet pas d'avoir accès à ces informations")
                        return []
                # Extraction des entités 'type_information' et 'periode_livraison' depuis le tracker
                type_information = next(tracker.get_latest_entity_values("type_information"), None)
                periode_entite = next(tracker.get_latest_entity_values("periode_livraison"), None)

                print(type_information)
                print(periode_entite)

                if periode_entite  and type_information in ["bons de commande", "commandes"]:
                    # Définir la condition de la période
                    periode_condition = ""
                    if periode_entite == "aujourd'hui":
                        periode_condition = "DATE(stock_order_delivery_date) = CURDATE()"
                    elif periode_entite == "cette semaine":
                        periode_condition = "YEARWEEK(stock_order_delivery_date, 1) = YEARWEEK(CURDATE(), 1)"
                    elif periode_entite == "semaine prochaine":
                        periode_condition = "YEARWEEK(stock_order_delivery_date, 1) = YEARWEEK(DATE_ADD(CURDATE(), INTERVAL 1 WEEK), 1)"
                    elif periode_entite == "ce mois":
                        periode_condition = "MONTH(stock_order_delivery_date) = MONTH(CURDATE())"
                    elif periode_entite == "mois prochain":
                        periode_condition = "MONTH(stock_order_delivery_date) = MONTH(DATE_ADD(CURDATE(), INTERVAL 1 MONTH))"
                    else:
                        dispatcher.utter_message(text=f"La période '{periode_entite}' n'est pas reconnue pour le moment.")
                        return []

                    # Requête SQL pour récupérer les bons de commande dans la période spécifiée
                    sql_query = f"""
                        SELECT stock_order_number, stock_order_ref, stock_order_date, stock_order_delivery_date, stock_order_requester
                        FROM stock_order
                        WHERE {periode_condition}
                    """
                    cursor.execute(sql_query)
                    commandes = cursor.fetchall()

                    if commandes:
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
                        <h3>Bons de commande pour '{periode_entite}'</h3>
                        <table>
                            <tr>
                                <th>Numéro</th>
                                <th>Référence</th>
                                <th>Date de commande</th>
                                <th>Date de livraison</th>
                                <th>Demandeur</th>
                            </tr>
                        """

                        for commande in commandes:
                            stock_order_number = commande[0]
                            stock_order_ref = commande[1]
                            stock_order_date = commande[2]
                            stock_order_delivery_date = commande[3]
                            stock_order_requester = commande[4]

                            message += f"""
                            <tr>
                                <td>{stock_order_number}</td>
                                <td>{stock_order_ref}</td>
                                <td>{stock_order_date}</td>
                                <td>{stock_order_delivery_date}</td>
                                <td>{stock_order_requester}</td>
                            </tr>
                            """
                        message += "</table>"
                        dispatcher.utter_message(text=message, parse_mode="HTML")

                    else:
                        dispatcher.utter_message(text=f"Aucun bon de commande trouvé pour '{periode_entite}'.")

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

class ActionSavoirCommandesRetardLivraison(Action):
    def name(self) -> Text:
        return "action_savoir_commandes_retard_livraison"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = 17
        type_information = next(tracker.get_latest_entity_values('type_information'), None)
        print(type_information)
        if type_information in ["bons de commandes", "commandes", "bons de commande"]:
            try:
                # Connexion à la base de données
                conn = create_connection()

                if conn:
                    cursor = conn.cursor()
                    # Requête SQL pour obtenir le user_profile_id
                    sql_query = f"""
                        SELECT up.user_profile_id
                        FROM user u
                        JOIN user_company uc ON u.user_id = uc.user_company_user_id
                        JOIN user_profile up ON uc.user_company_profile_id = up.user_profile_id
                        WHERE u.user_id = {user_id}
                    """
                    cursor.execute(sql_query)
                    row = cursor.fetchone()

                    if row:
                        user_profile_id = row[0]

                        # Vérification si l'utilisateur a le bon profil
                        if user_profile_id != 8:
                            dispatcher.utter_message(text="Désolé, votre profil ne vous permet pas d'avoir accès à ces informations.")
                            return []

                    # Requête SQL pour récupérer les commandes en retard de livraison
                    sql_query = """
                        SELECT
                            stock_order_number,
                            stock_order_ref,
                            stock_order_date,
                            stock_order_delivery_date,
                            stock_order_requester
                        FROM
                            stock_order
                        WHERE
                            stock_order_delivery_date < CURDATE()
                            AND stock_order_situation_id != 7
                    """

                    # Exécution de la requête SQL
                    cursor.execute(sql_query)
                    commandes_retard = cursor.fetchall()

                    if commandes_retard:
                        message = """
                        <style>
                            h3 {
                                font-size: 18px;
                            }
                            table {
                                border-collapse: collapse;
                                width: 100%;
                            }
                            th, td {
                                border: 1px solid black;
                                padding: 8px;
                                text-align: left;
                            }
                            th {
                                background-color: white;
                                color: navy;
                            }
                        </style>
                        <h3>Commandes en retard de livraison</h3>
                        <table>
                            <tr>
                                <th>Numéro de commande</th>
                                <th>Référence</th>
                                <th>Date de commande</th>
                                <th>Date de livraison prévue</th>
                                <th>Demandeur</th>
                            </tr>
                        """

                        for commande in commandes_retard:
                            stock_order_number = commande[0]
                            stock_order_ref = commande[1]
                            stock_order_date = commande[2]
                            stock_order_delivery_date = commande[3]
                            stock_order_requester = commande[4]

                            message += f"""
                            <tr>
                                <td>{stock_order_number}</td>
                                <td>{stock_order_ref}</td>
                                <td>{stock_order_date}</td>
                                <td>{stock_order_delivery_date}</td>
                                <td>{stock_order_requester}</td>
                            </tr>
                            """
                        message += "</table>"
                        dispatcher.utter_message(text=message, parse_mode="HTML")

                    else:
                        dispatcher.utter_message(text="Aucune commande en retard de livraison.")

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

        else:
            dispatcher.utter_message(text="Les expressions prises en charge sont 'bons de commande' ou 'commandes'.")
            return []

