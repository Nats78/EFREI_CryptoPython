from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify, request

import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Génération de la clé pour le chiffrement/déchiffrement
key = Fernet.generate_key()
f = Fernet(key)

# Route pour chiffrer une valeur
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur du token
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

# Nouvelle route pour déchiffrer un token
@app.route('/decrypt/', methods=['POST'])
def decryptage():
    data = request.get_json()  # Récupère le JSON envoyé dans la requête
    token = data['token']  # Récupère le token crypté depuis la requête
    try:
        # Décryptage du token
        token_bytes = token.encode()  # Convertir le token en bytes
        decrypted_value = f.decrypt(token_bytes).decode()  # Décrypter et décoder en str
        return jsonify({'decrypted_value': decrypted_value})  # Retourne la valeur décryptée
    except Exception as e:
        return jsonify({'error': 'Token invalide ou erreur de décryptage.'}), 400

# Route spécifique pour décrypter la date de naissance 01/12/2003
@app.route('/decrypt_date_naissance')
def decrypt_date_naissance():
    token = request.args.get('token')
    try:
        token_bytes = token.encode()  # Convertir le token en bytes
        decrypted_value = f.decrypt(token_bytes).decode()  # Décrypter et décoder en str
        if decrypted_value == "01/12/2003":
            return jsonify({'decrypted_value': decrypted_value})  # Retourne la valeur décryptée
        else:
            return jsonify({'error': 'Date de naissance incorrecte.'}), 400
    except Exception as e:
        return jsonify({'error': 'Token invalide ou erreur de décryptage.'}), 400

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
