import mysql.connector
from mysql.connector import Error

# Configuration de la connexion
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'myapp_db',
}

def create_connection():
    """ Créer une connexion à la base de données MySQL """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            print("Connexion à la base de données MySQL réussie")
    except Error as e:
        print(f"L'erreur '{e}' est survenue")
    return connection
