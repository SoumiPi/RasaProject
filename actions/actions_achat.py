# #import jwt
from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from connexion_db import create_connection

# JWT_SECRET_KEY = '123456789'

# def get_user_role_from_token(token):
#     """Decode the JWT token to get the user role."""
#     try:
#         decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
#         return decoded.get('role')
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.InvalidTokenError:
#         return None

# class ActionDemandeAchatFournisseur(Action):
#     def name(self) -> Text:
#         return "action_demander_fournisseur_demande_achat"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # Récupération du token JWT depuis les métadonnées du tracker
#         token = tracker.latest_message.get('metadata', {}).get('token')
#         user_role = get_user_role_from_token(token)
#         print(f"Rôle de l'utilisateur : {user_role}")

#         # Vérification du rôle pour autoriser l'action
#         if user_role not in ['technicien']:  # Ajoutez les rôles autorisés ici
#             dispatcher.utter_message(text="Désolé, vous n'avez pas le droit d'accès à ces informations.")
#             return []

#         try:
#             # Connexion à la base de données
#             conn = create_connection()

#             if conn:
#                 cursor = conn.cursor()

#                 # Extraction des entités depuis le tracker
#                 numero_demande = next(tracker.get_latest_entity_values('numero_demande'), None)
#                 demande_achat = next(tracker.get_latest_entity_values('demande_achat'), None)
#                 type_information = next(tracker.get_latest_entity_values('type_information'), None)

#                 # Vérification des entités pertinentes
#                 if demande_achat in ["demandes d'achat", "demande d'achat", "DA"] and type_information in ["fournisseur", "prestataire"]:
#                     if numero_demande:
#                         # Requête SQL pour récupérer le fournisseur de la demande spécifiée
#                         sql_query = f"""
#                             SELECT s.supplier_designation
#                             FROM purchase_requisition pr
#                             LEFT JOIN supplier s ON pr.purchase_requisition_supplier_id = s.supplier_id
#                             WHERE pr.purchase_requisition_number = '{numero_demande}'
#                             """

#                         # Exécution de la requête SQL
#                         cursor.execute(sql_query)
#                         fournisseur = cursor.fetchone()

#                         if fournisseur:
#                             supplier_designation = fournisseur[0]
#                             response = f"Le fournisseur pour la demande d'achat numéro {numero_demande} est {supplier_designation}."
#                             dispatcher.utter_message(text=response)
#                         else:
#                             dispatcher.utter_message(text=f"Aucune information trouvée pour le fournisseur de la demande d'achat numéro {numero_demande}.")
#                     else:
#                         dispatcher.utter_message(text="Le numéro de demande spécifié est invalide ou manquant.")
#                 else:
#                     dispatcher.utter_message(text="Je ne comprends pas votre demande, veuillez reformuler votre question.")

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


#ok
# class ActionDemandeAchatFournisseur(Action):
#     def name(self) -> Text:
#         return "action_demander_fournisseur_demande_achat"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         try:
#             # Connexion à la base de données
#             conn = create_connection()

#             if conn:
#                 cursor = conn.cursor()

#                 # Extraction de l'entité 'numero_demande' depuis le tracker
#                 numero_demande = next(tracker.get_latest_entity_values('numero_demande'), None)
#                 demande_achat = next(tracker.get_latest_entity_values('demande_achat'), None)
#                 type_information = next(tracker.get_latest_entity_values('type_information'), None)

#                 if demande_achat in ["demandes d'achat", "demande d'achat", "DA"] and type_information in ["fournisseur", "prestataire"]:
#                     if numero_demande:
#                         # Requête SQL pour récupérer le fournisseur de la demande spécifiée
#                         sql_query = f"""
#                             SELECT s.supplier_designation
#                             FROM purchase_requisition pr
#                             LEFT JOIN supplier s ON pr.purchase_requisition_supplier_id = s.supplier_id
#                             WHERE pr.purchase_requisition_number = '{numero_demande}'
#                             """

#                         # Exécution de la requête SQL
#                         cursor.execute(sql_query)
#                         fournisseur = cursor.fetchone()

#                         if fournisseur:
#                             supplier_designation = fournisseur[0]
#                             response = f"Le fournisseur pour la demande d'achat numéro {numero_demande} est {supplier_designation}."
#                             dispatcher.utter_message(text=response)
#                         else:
#                             dispatcher.utter_message(text=f"Aucune information trouvée pour le fournisseur de la demande d'achat numéro {numero_demande}.")
#                     else:
#                         dispatcher.utter_message(text="Le numéro de demande spécifié est invalide ou manquant.")

#                     cursor.close()
#                     conn.close()
#                 else:
#                     dispatcher.utter_message(text="Je n'arrive pas comprendre ce que vous dites, verifiez bien votre question.")

#             else:
#                 dispatcher.utter_message(text="Problème de connexion à la base de données.")

#         except mysql.connector.Error as e:
#             print(f"Erreur MySQL : {e}")
#             dispatcher.utter_message(text="Erreur MySQL lors de la récupération des informations depuis la base de données.")

#         except Exception as e:
#             print(f"Erreur : {e}")
#             dispatcher.utter_message(text="Erreur lors de la récupération des informations depuis la base de données.")

#         return []


#pas ok
class ActionDemandeAchatDelaiLivraison(Action):
    def name(self) -> Text:
        return "action_demande_delai_livraison_demande_achat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

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

        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

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
        try:
            # Connexion à la base de données
            conn = create_connection()

            if conn:
                cursor = conn.cursor()

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

        except Error as e:
            print(f"Erreur MySQL : {e}")
            dispatcher.utter_message(text="Erreur MySQL lors de la récupération des informations depuis la base de données.")

        except Exception as e:
            print(f"Erreur : {e}")
            dispatcher.utter_message(text="Erreur lors de la récupération des informations depuis la base de données.")

        return []


