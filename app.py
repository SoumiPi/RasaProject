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
        response_obj = {'text': response['text']}
        if 'buttons' in response:
            response_obj['buttons'] = response['buttons']
        bot_responses.append(response_obj)

    # Retourner la réponse du bot
    return jsonify({'responses': bot_responses})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
