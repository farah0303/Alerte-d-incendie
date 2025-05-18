
# 🚨 Projet Digital Twin – Simulation de Capteurs Incendie

## 🚀 Contexte

Dans un monde de plus en plus connecté, la détection précoce des risques d'incendie devient essentielle, notamment dans les environnements industriels et tertiaires.

Ce projet propose une simulation réaliste d’un système de capteurs de fumée, s’appuyant sur des technologies modernes telles que **Orion Context Broker**, **MongoDB**, et **Flask**, pour illustrer le concept puissant de **Digital Twin (jumeau numérique)**.



## 🧠 Objectif du Projet

L’objectif principal est de mettre en place un système intelligent capable de simuler et surveiller la présence de fumée dans un environnement sécurisé. Voici les fonctionnalités clés :

- 🔁 Simuler un capteur de fumée qui génère des niveaux de fumée entre 0 et 100 % toutes les 10 secondes.
- 🚨 Détecter toute mesure supérieure à un seuil critique (ex: 50 %) et déclencher une alerte immédiate via un serveur Flask.
- 🧾 Enregistrer toutes les données dans une base MongoDB, directement depuis Flask.
- 🧠 Gérer dynamiquement les entités et les mesures avec Orion Context Broker via l’API NGSI v2.

Ce projet démontre comment un Digital Twin peut être utilisé pour automatiser, surveiller, alerter et stocker des données dans un système distribué, typique des architectures IoT industrielles.



## ⚙️ Architecture du Système

### 🧩 Composants Clés

#### 🟢 Orion Context Broker

- Centralise toutes les entités (capteurs) et leurs données.
- Permet l’interaction via l’API NGSI pour gérer les informations en temps réel.

#### 🟣 MongoDB

- Sert de base de données de stockage historique.
- Garde une trace complète de toutes les lectures des capteurs.

#### 🔴 Flask

- Sert à recevoir des alertes en temps réel via une API HTTP POST.
- Affiche les alertes d'incendie dans les logs et peut être étendu pour effectuer des actions automatiques (comme envoyer un email ou une notification).
- Gère également l’insertion des données directement dans MongoDB.




## 🌐 Pourquoi c’est important ?

Ce projet est une illustration concrète des technologies de l’IoT moderne, qui combinent temps réel, réactivité, persistance des données, et supervision intelligente. Il reflète :

- Le potentiel des architectures basées sur FIWARE (Orion Context Broker).
- L’importance d’un monitoring intelligent dans les systèmes industriels.
- La simplicité avec laquelle on peut simuler un Digital Twin efficace à l’aide de conteneurs Docker et de technologies comme Flask.



## 📦 Modèles de données JSON utilisés

Le projet utilise plusieurs modèles de données au format **JSON** pour assurer la communication entre les différents services.

### 1. Données envoyées par le simulateur de capteurs à Orion

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

### 2. Alertes envoyées à Flask

```json
{
  "id": "SmokeSensor3",
  "smokeLevel": 82.1
}
```

### 3. Données stockées dans MongoDB

```json
{
  "_id": "ObjectId(...)",
  "id": "SmokeSensor3",
  "type": "SmokeSensor",
  "smokeLevel": 82.1,
  "timestamp": "2025-04-05T12:00:00Z"
}
```

Ces modèles assurent une intégration cohérente entre les services Docker tout en respectant les standards NGSI v2 de FIWARE.


Voici **uniquement la partie explicative du fichier `docker-compose.yml`**, prête à être ajoutée dans ton `README.md` ou tout autre document :

---

## 📁 Fichier `docker-compose.yml`

Le fichier `docker-compose.yml` est utilisé pour définir et orchestrer les différents services Docker nécessaires à notre projet de Digital Twin. Il permet de déployer facilement un environnement contenant **Orion Context Broker**, **MongoDB**, une application **Flask** et un simulateur de capteurs, tous interconnectés.

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
- **Orion Context Broker** : gestion des entités (capteurs).
- **MongoDB** : stockage des alertes.
- **Flask App** : serveur web pour recevoir les alertes.
- **Sensor Simulation** : simulation des données envoyées aux capteurs.

Ils sont connectés via un réseau Docker privé avec une configuration IP personnalisée.


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

- Utilise l’image officielle de FIWARE Orion.
- Dépend de MongoDB (`mongo-db`) comme base de données.
- Disponible sur le port `1026`.
- Configure Orion pour utiliser MongoDB en mode debug sans cache.
- Vérifie sa disponibilité via `/version`.



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

- Base de données utilisée par Orion et Flask.
- Stocke les alertes générées par le système.
- Persistance des données via un volume Docker.
- Vérifie que la base est opérationnelle toutes les 5 secondes.



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

- Application Flask qui reçoit les alertes et synchronise les données avec Orion.
- Construite depuis le dossier `flask_app`.
- Environnement de développement activé.
- Redémarre automatiquement en cas d’échec.
- Teste l’endpoint `/sync` pour vérifier si l’application est prête.



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

- Simule trois capteurs envoyant des niveaux de fumée aléatoires.
- Dépend du démarrage d’Orion et de Flask.
- Variables d’environnement configurées pour communiquer avec ces deux services.
- Redémarre toujours automatiquement.



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

- Tous les services partagent le même réseau Docker.
- Communication entre services via leurs noms (`orion`, `flask-app`, etc.)
- Configuration IP personnalisée avec sous-réseau `172.19.0.0/24`.



### 💾 Volumes

```yaml
volumes:
  mongo-db: ~
```

- Le volume `mongo-db` permet de persister les données MongoDB.
- Garantit la sauvegarde des alertes en cas de redémarrage ou arrêt du conteneur.



Souhaitez-vous que je vous fournisse cette section au format `.md` ou `.txt` prêt à télécharger ? 😊

## 🧪 Fonctionnement du projet

Le fichier `sensor_simulation.py` joue un rôle central dans ce projet, en simulant **trois capteurs de fumée virtuels** (`SmokeSensor1`, `SmokeSensor2`, `SmokeSensor3`). Ces capteurs génèrent automatiquement des niveaux de fumée compris entre **0 et 100 %**, représentant une mesure aléatoire d’une situation réelle de détection de fumée.

### 🔁 Déroulement du processus :

1. **Initialisation des capteurs :**
   - Le script commence par définir une liste de capteurs avec leurs identifiants uniques et leur type (`SmokeSensor`).
   - Un seuil critique est également configuré (`SMOKE_LEVEL_THRESHOLD = 80`) pour déclencher une alerte en cas de niveau de fumée élevé.

2. **Génération aléatoire :**
   - À chaque itération, le script utilise la fonction `generate_smoke_level()` pour produire une valeur aléatoire entre 0 et 100, simulant la lecture d’un capteur physique.

3. **Envoi vers Orion Context Broker :**
   - Les données sont envoyées via une requête HTTP POST à l’API NGSI d’Orion (`http://orion:1026/v2/op/update`), sous forme de payload JSON.
   - Ce payload contient :
     - L’identifiant du capteur.
     - La valeur simulée du niveau de fumée.
     - Une date de création au format ISO 8601.

4. **Détection d’anomalie :**
   - Si la valeur générée dépasse le seuil défini, une alerte est immédiatement envoyée à Flask via une requête POST sur l’URL `http://flask-app:5000/alert`.
   - Cette alerte inclut l’ID du capteur et le niveau de fumée mesuré.

5. **Boucle infinie :**
   - Le processus se répète toutes les **5 secondes**, permettant une surveillance continue des niveaux de fumée.

## 4. 🛠️ Process d'installation de la solution

### ✅ Prérequis

- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 📁 Structure du projet attendue

```
digital_twin/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── sensor_simulation.py
├── flask_app/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
```

### 🔧 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/farah0303/Alerte-d-incendie.git
cd Alerte-d-incendie
```

2. Vérifiez que tous les fichiers nécessaires sont présents.

3. (Facultatif) Modifiez les variables d’environnement si nécessaire.



## 5. ▶️ Comment lancer l'application

Depuis le répertoire racine du projet :

```bash
docker-compose up --build
```

> ⏱️ À la première exécution, Docker télécharge les images nécessaires et construit les conteneurs personnalisés (`flask-app` et `sensor-simulation`). Cela peut prendre quelques minutes.


### 🧪 Vérifier que tout fonctionne

Après quelques secondes, vous pouvez vérifier le bon fonctionnement des services en accédant aux points suivants :

- **Orion** : [http://localhost:1026/version](http://localhost:1026/version) → devrait afficher la version d’Orion (ex: `{"orion": "3.3.0"}`).
- **Flask** : [http://localhost:5000/sync](http://localhost:5000/sync) → déclenche la synchronisation des données entre Orion et MongoDB.
- **MongoDB** : `mongodb://localhost:27017` → accessible via un outil comme **MongoDB Compass** pour visualiser les alertes enregistrées.

📁 **De plus, un dossier intitulé `screenshots` contient des captures d’écran illustrant le bon déroulement du projet**, notamment :
- L’interface de Flask affichant les alertes,
- Les logs Docker confirmant l’envoi des données à Orion,
- La base MongoDB avec les alertes stockées.

Ces images permettent d’avoir une vue claire sur le comportement attendu de l’application à chaque étape.

### 🔁 Arrêter l’application

```bash
docker-compose down
```
