from flask import Flask, request, jsonify
from pymongo import MongoClient
import logging
import requests
import time
app = Flask(__name__)

# Configuration de la connexion à MongoDB
client = MongoClient("mongodb://mongo-db:27017/")
db = client["smoke_sensor_db"]
collection = db["readings"]

# Configuration des logs
logging.basicConfig(level=logging.INFO)

@app.route('/alert', methods=['POST'])
def handle_alert():
    """
    Endpoint appelé par Orion lorsqu'une alerte est déclenchée (fumée > seuil)
    """
    data = request.json
    sensor_id = data.get('id')
    smoke_level = data.get('smokeLevel')

    if smoke_level is not None:
        app.logger.info(f"🚨 ALERTE INCENDIE : Capteur {sensor_id} a détecté un niveau de fumée élevé : {smoke_level}%")
        # Optionnel : insérer directement dans MongoDB
        collection.insert_one({
            "id": sensor_id,
            "type": "SmokeSensor",
            "smokeLevel": smoke_level,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        return jsonify({"status": "Alerte reçue et enregistrée"}), 200
    else:
        app.logger.warning("⚠️ Données incomplètes reçues")
        return jsonify({"error": "Données manquantes"}), 400

@app.route('/sync', methods=['GET'])
def sync_with_orion():
    """
    Endpoint pour récupérer toutes les entités depuis Orion et les sauvegarder dans MongoDB
    """
    try:
        res = requests.get("http://orion:1026/v2/entities?type=SmokeSensor")
        if res.status_code != 200:
            return jsonify({"error": "Impossible d'atteindre Orion"}), 500

        sensors = res.json()

        for sensor in sensors:
            doc = {
                "id": sensor["id"],
                "type": sensor["type"],
                "smokeLevel": sensor["smokeLevel"]["value"],
                "timestamp": sensor["smokeLevel"]["metadata"]["dateCreated"]["value"]
            }
            collection.insert_one(doc)

        return jsonify({"status": "Données synchronisées avec MongoDB"}), 200
    except Exception as e:
        app.logger.error(f"[ERREUR] Impossible de synchroniser avec Orion : {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)