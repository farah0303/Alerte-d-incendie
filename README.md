 🚨 Projet Digital Twin – Simulation de Capteurs Incendie:

🚀 Contexte:

Dans un monde de plus en plus connecté, la détection précoce des risques d'incendie devient essentielle, notamment dans les environnements industriels et tertiaires. Ce projet propose une simulation réaliste d’un système de capteurs de fumée, s’appuyant sur des technologies modernes telles que Orion Context Broker , MongoDB , et Flask , pour illustrer le concept puissant de Digital Twin (jumeau numérique)

🧠 L'idée est de représenter virtuellement un réseau de capteurs physiques installés dans un bâtiment, de surveiller en temps réel la présence de fumée, de déclencher automatiquement une alerte en cas de détection anormale, et d’enregistrer toutes les mesures dans une base de données.

🎯 Objectif du Projet:

L’objectif principal est de mettre en place un système intelligent capable de simuler et surveiller la présence de fumée dans un environnement sécurisé. Voici les fonctionnalités clés :

🔁 Simuler un capteur de fumée qui génère des niveaux de fumée entre 0 et 100 % toutes les 10 secondes.

🚨 Détecter toute mesure supérieure à un seuil critique (ex: 50 %) et déclencher une alerte immédiate via un serveur Flask.

🧾 Enregistrer toutes les données dans une base MongoDB, directement depuis Flask.

🧠 Gérer dynamiquement les entités et les mesures avec Orion Context Broker via l’API NGSI v2.

Ce projet démontre comment un Digital Twin peut être utilisé pour automatiser, surveiller, alerter et stocker des données dans un système distribué, typique des architectures IoT industrielles.

⚙️ Architecture du Système:

🧩 Composants Clés:

🟢 Orion Context Broker:

Centralise toutes les entités (capteurs) et leurs données.

Permet l’interaction via l’API NGSI pour gérer les informations en temps réel.

🟣 MongoDB:

Sert de base de données de stockage historique.

Garde une trace complète de toutes les lectures des capteurs.

🔴 Flask:

Sert à recevoir des alertes en temps réel via une API HTTP POST.

Affiche les alertes d'incendie dans les logs et peut être étendu pour effectuer des actions automatiques (comme envoyer un email ou une notification).

Gère également l’insertion des données directement dans MongoDB .

🔄 Flux de Données:

🎛️ Un capteur virtuel génère un niveau de fumée aléatoire toutes les 10 secondes

📡 Ces données sont envoyées vers Orion Context Broker via des requêtes HTTP NGSI

📬 Flask reçoit une alerte lorsque le seuil critique est dépassé.

💾 Flask stocke directement les données dans MongoDB, 

🚨 Lorsque le niveau de fumée dépasse le seuil de 30°C, une alerte est envoyée au serveur Flask, qui l'affiche dans les logs.

🌐 Pourquoi c’est important:

Ce projet est une illustration concrète des technologies de l’IoT moderne, qui combinent temps réel, réactivité, persistance des données, et supervision intelligente. Il reflète :

Le potentiel des architectures basées sur FIWARE (Orion Context Broker).

L’importance d’un monitoring intelligent dans les systèmes industriels.

La simplicité avec laquelle on peut simuler un Digital Twin efficace à l’aide de conteneurs Docker et de technologies comme Flask.


Le projet utilise plusieurs modèles de données au format **JSON** pour assurer la communication entre les différents services. Le premier modèle est utilisé par le simulateur de capteurs (`sensor_simulation.py`) pour envoyer des données à **Orion Context Broker**, en représentant trois capteurs de fumée :
```json
{
  "actionType": "append",
  "entities": [
    {
      "id": "SmokeSensor1",
      "type": "SmokeSensor",
      "smokeLevel": {
        "value": 75.3,
        "type": "Number",
        "metadata": {
          "dateCreated": {
            "type": "DateTime",
            "value": "2025-04-05T12:00:00Z"
          }
        }
      }
    },
    {
      "id": "SmokeSensor2",
      "type": "SmokeSensor",
      "smokeLevel": {
        "value": 68.9,
        "type": "Number",
        "metadata": {
          "dateCreated": {
            "type": "DateTime",
            "value": "2025-04-05T12:00:00Z"
          }
        }
      }
    },
    {
      "id": "SmokeSensor3",
      "type": "SmokeSensor",
      "smokeLevel": {
        "value": 82.1,
        "type": "Number",
        "metadata": {
          "dateCreated": {
            "type": "DateTime",
            "value": "2025-04-05T12:00:00Z"
          }
        }
      }
    }
  ]
}
```
Ce format permet d’ajouter ou de mettre à jour les entités dans Orion. Lorsqu’un niveau de fumée dépasse un seuil prédéfini, une alerte est envoyée à l’application Flask via ce modèle :
```json
{
  "id": "SmokeSensor3",
  "smokeLevel": 82.1
}
```
Enfin, l’application Flask stocke ces alertes dans **MongoDB** sous forme de documents structurés comme suit :
```json
{
  "_id": "ObjectId(...)",
  "id": "SmokeSensor3",
  "type": "SmokeSensor",
  "smokeLevel": 82.1,
  "timestamp": "2025-04-05T12:00:00Z"
}
```
Ces modèles JSON assurent une intégration cohérente et fluide entre les services Docker (simulateur, Orion, Flask et MongoDB), tout en respectant les standards NGSI v2 de FIWARE.

## 📁 Fichier `docker-compose.yml`

Le fichier `docker-compose.yml` est au cœur du déploiement de notre projet. Il permet de définir et exécuter facilement **plusieurs services Docker interconnectés** : Orion Context Broker, MongoDB, Flask (application d’alerte) et la simulation des capteurs.

### 🔧 Structure générale

```yaml
version: "3.8"
services:
  orion:
    ...
  mongo-db:
    ...
  flask-app:
    ...
  sensor-simulation:
    ...
networks:
  default:
    ...
volumes:
  mongo-db: ~
```

Ce fichier définit **quatre services principaux** :

- **Orion Context Broker** : gestion du contexte des entités (capteurs).
- **MongoDB** : base de données pour stocker les alertes.
- **Flask App** : serveur web qui gère les alertes et la synchronisation avec Orion.
- **Sensor Simulation** : simulateur de capteurs envoyant des niveaux de fumée.

Tous ces services sont connectés via un réseau Docker par défaut avec une configuration IP personnalisée.

---

### 📦 Services Détaillés

#### 1. **Orion Context Broker**

```yaml
orion:
  labels:
    org.fiware: 'tutorial'
  image: fiware/orion:${ORION_VERSION:-3.3.0}
  hostname: orion
  container_name: fiware-orion
  depends_on:
    - mongo-db
  networks:
      - default
  ports:
    - "${ORION_PORT:-1026}:${ORION_PORT:-1026}"
  command: -dbhost mongo-db -logLevel DEBUG -noCache
  healthcheck:
    test: curl --fail -s http://orion:${ORION_PORT:-1026}/version || exit 1
    interval: 5s
```

- **Rôle** : Gestion centralisée des entités (ex: capteurs).
- **Dépendance** : MongoDB (`mongo-db`)
- **Port** : Disponible sur `http://localhost:1026`
- **Commande** : Utilise MongoDB comme base de données et active les logs détaillés.
- **Healthcheck** : Teste `/version` toutes les 5 secondes pour vérifier si le service est actif.

---

#### 2. **MongoDB**

```yaml
mongo-db:
  labels:
    org.fiware: 'tutorial'
  image: mongo:${MONGO_DB_VERSION:-6.0}
  hostname: mongo-db
  container_name: db-mongo
  expose:
    - "${MONGO_DB_PORT:-27017}"
  ports:
    - "${MONGO_DB_PORT:-27017}:${MONGO_DB_PORT:-27017}"
  networks:
    - default
  volumes:
    - mongo-db:/data
  healthcheck:
    test: |
      host=`hostname --ip-address || echo '127.0.0.1'`; 
      mongo --quiet $host/test --eval 'quit(db.runCommand({ ping: 1 }).ok ? 0 : 2)' && echo 0 || echo 1
    interval: 5s
```

- **Rôle** : Stockage persistant des alertes reçues par Flask.
- **Volume** : `/data` est persisté via un volume Docker pour éviter la perte de données.
- **Port** : Disponible sur `27017`.
- **Healthcheck** : Vérifie que la base est prête à accepter les connexions.

---

#### 3. **Flask App**

```yaml
flask-app:
  build: ./flask_app
  container_name: flask-app
  ports:
    - "5000:5000"
  depends_on:
    - orion
  networks:
    - default
  environment:
    - FLASK_ENV=development
  restart: on-failure:5
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5000/sync"]
    interval: 10s
    timeout: 5s
    retries: 5
```

- **Rôle** : Réception des alertes de niveau de fumée trop élevé et synchronisation avec Orion.
- **Build** : Construit depuis le sous-dossier `flask_app`.
- **Port** : Disponible sur `http://localhost:5000`.
- **Environnement** : Mode développement activé.
- **Healthcheck** : Vérifie l’endpoint `/sync` toutes les 10 secondes.

---

#### 4. **Sensor Simulation**

```yaml
sensor-simulation:
  build: .
  container_name: sensor-simulation
  depends_on:
    - orion
    - flask-app
  networks:
    - default
  environment:
    - ORION_URL=http://orion:1026/v2/op/update
    - FLASK_ALERT_URL=http://flask-app:5000/alert
  restart: always
```

- **Rôle** : Simule trois capteurs envoyant des niveaux de fumée aléatoires.
- **Dépendances** : Orion et Flask doivent être démarrés avant lui.
- **Build** : Construit depuis le répertoire racine.
- **Variables d’environnement** :
  - `ORION_URL` : URL de mise à jour d’Orion.
  - `FLASK_ALERT_URL` : URL de notification en cas d’alerte.
- **Restart policy** : Redémarre automatiquement si le conteneur s’arrête.

---

### 🌐 Réseau

```yaml
networks:
  default:
    labels:
      org.fiware: 'tutorial'
    ipam:
      config:
        - subnet: 172.19.0.0/24
```

- Les services communiquent entre eux via un réseau Docker privé.
- Sous-réseau configuré : `172.19.0.0/24`.
- Chaque service peut atteindre les autres par leur nom DNS (`orion`, `flask-app`, etc.)

---

### 💾 Volumes

```yaml
volumes:
  mongo-db: ~
```

- Un volume nommé `mongo-db` est utilisé pour persister les données MongoDB.
- Cela garantit que les alertes ne soient pas perdues en cas d’arrêt ou de redémarrage du conteneur.

---

Voici les sections **4. Process d'installation de la solution** et **5. Comment lancer l'application**, que tu peux ajouter directement à ton `README.md`.

---

## 4. 🛠️ Process d'installation de la solution

Pour déployer et exécuter cette solution, nous utilisons **Docker Compose**, un outil permettant de gérer facilement des applications multi-conteneurs.

### ✅ Prérequis

Avant de commencer, assurez-vous d’avoir installé :

- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)
💡 Sur Windows, Docker Desktop inclut Docker Compose.

### 📁 Structure du projet attendue

```
digital_twin/
├── Dockerfile                  # Pour le simulateur de capteurs
├── docker-compose.yml          # Configuration globale
├── requirements.txt            # Dépendances Python pour le simulateur
├── sensor_simulation.py        # Simule les capteurs
├── flask_app/
│   ├── Dockerfile              # Pour Flask
│   ├── app.py                  # Code Flask
│   └── requirements.txt        # Dépendances Flask
```

### 🔧 Installation

1. Clonez ou téléchargez le dépôt :
```bash
git clone https://github.com/farah0303/Alerte-d-incendie.git
cd Alerte-d-incendie
```

2. Vérifiez que tous les fichiers nécessaires sont présents dans le répertoire (`docker-compose.yml`, `sensor_simulation.py`, etc.).

3. (Facultatif) Vous pouvez modifier les variables d’environnement dans le fichier `.env` ou directement dans `docker-compose.yml`.

---

## 5. ▶️ Comment lancer l'application

Une fois le projet prêt, vous pouvez démarrer toute l’infrastructure avec une seule commande.

### 🚀 Démarrage

Depuis le répertoire racine du projet :

```bash
venv\Scripts\activate
docker-compose up --build
```

> ⏱️ À la première exécution, Docker télécharge les images nécessaires et construit les conteneurs personnalisés (`flask-app` et `sensor-simulation`). Cela peut prendre quelques minutes.

### 📦 Détail du démarrage

1. **MongoDB** démarre en premier.
2. **Orion Context Broker** se connecte à MongoDB.
3. **Flask App** démarre et vérifie qu’Orion est prêt via `/sync`.
4. **Sensor Simulation** commence à envoyer des données à Orion toutes les 10 secondes.
5. Si un seuil est dépassé, une alerte est envoyée à Flask et enregistrée dans MongoDB.


### 🧪 Vérifier que tout fonctionne

Après quelques secondes, vous pouvez vérifier :

- **Orion** : http://localhost:1026/version → devrait afficher la version d’Orion.
- **Flask** : http://localhost:5000/sync → synchronise les données depuis Orion.
- **MongoDB** : accédez-y via un client comme MongoDB Compass à l’adresse `mongodb://localhost:27017`.

---

### 🔁 Arrêter l’application

Pour arrêter l’application proprement :

```bash
docker-compose down
```


