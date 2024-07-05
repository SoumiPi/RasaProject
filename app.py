# from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# from connexion_db import create_connection
# #import jwt
# import datetime
# import requests

# app = Flask(__name__)
# app.secret_key = ''  # Clé secrète pour signer les cookies de session

# RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'  # URL de votre serveur Rasa
# JWT_SECRET_KEY = '123456789'

# def generate_token(user_role):
#     """Generate JWT token."""
#     payload = {
#         'role': user_role,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
#     }
#     token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
#     return token  # PyJWT 2.x returns a string directly

# @app.route('/')
# def login():
#     return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def do_login():
#     username = request.form['username']
#     password = request.form['password']

#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT user, password, role FROM portail WHERE user=%s", (username,))
#     user = cursor.fetchone()

#     if user is None:
#         flash('Nom d’utilisateur incorrect.')
#         return redirect(url_for('login'))
#     elif user[1] != password:
#         flash('Mot de passe incorrect.')
#         return redirect(url_for('login'))
#     else:
#         session['username'] = username
#         session['role'] = user[2]  # Enregistrez le rôle de l'utilisateur dans la session

#         # Générer un token JWT avec le rôle de l'utilisateur
#         token = generate_token(user[2])
#         return jsonify({'token': token})  # Retourner le token en réponse JSON

# @app.route('/index')
# def index():
#     if 'username' in session:
#         return render_template('chat.html', username=session['username'], role=session['role'])
#     else:
#         return redirect(url_for('login'))

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     if not 'username' in session:
#         return jsonify({'responses': [{'text': 'Veuillez vous connecter pour accéder au chatbot.'}], 'unknown': True})

#     user_message = request.json.get('message')
#     token = request.json.get('token')  # Le token doit être transmis dans la requête

#     if not token:
#         return jsonify({'responses': [{'text': 'Token manquant. Veuillez vous reconnecter.'}], 'unknown': True})

#     print("Message de l'utilisateur:", user_message)

#     # Envoyer le message de l'utilisateur et le rôle à Rasa
#     payload = {
#         'message': user_message,
#         'sender': session.get('username', 'default'),
#         'metadata': {
#             'role': session.get('role'),  # Utiliser le rôle de l'utilisateur depuis la session
#             'token': token  # Inclure le token dans les métadonnées
#         }
#     }
#     try:
#         rasa_response = requests.post(RASA_API_URL, json=payload)
#         rasa_response.raise_for_status()  # Vérifiez si la requête a réussi
#         rasa_response_json = rasa_response.json()
#         print("Réponse de Rasa:", rasa_response_json)

#         bot_responses = []
#         for response in rasa_response_json:
#             response_obj = {'text': response.get('text', 'Désolé, je n\'ai pas la réponse à cette question.')}
#             if 'buttons' in response:
#                 response_obj['buttons'] = response['buttons']
#             bot_responses.append(response_obj)

#         all_unknown = all(r['text'] == 'Désolé, je n\'ai pas la réponse à cette question.' for r in bot_responses)

#         return jsonify({'responses': bot_responses, 'unknown': all_unknown})

#     except requests.exceptions.RequestException as e:
#         print(f"Erreur lors de la requête vers Rasa : {e}")
#         return jsonify({'responses': [{'text': 'Erreur lors de la communication avec le chatbot.'}], 'unknown': True})

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=3000)









from flask import Flask, render_template, request, jsonify
import requests

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    # Extraire le message de l'utilisateur de la requête
    user_message = request.json['message']
    print("Message de l'utilisateur:", user_message)

    # Envoyer le message de l'utilisateur à Rasa et obtenir la réponse du bot
    rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
    rasa_response_json = rasa_response.json()
    print("Réponse de Rasa:", rasa_response_json)

    # Extraire la réponse du bot
    bot_responses = []
    for response in rasa_response_json:
        response_obj = {'text': response.get('text', 'Désolé, je n\'ai pas la réponse à cette question.')}
        if 'buttons' in response:
            response_obj['buttons'] = response['buttons']
        bot_responses.append(response_obj)

    # Vérifier si toutes les réponses sont des réponses par défaut (non entraînées)
    all_unknown = all(r['text'] == 'Désolé, je n\'ai pas la réponse à cette question.' for r in bot_responses)

    # Retourner la réponse du bot avec un indicateur de non-réponse si nécessaire
    return jsonify({'responses': bot_responses, 'unknown': all_unknown})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
