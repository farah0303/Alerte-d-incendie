
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

#### 🔄 Flux de Données

1. Un capteur virtuel génère un niveau de fumée aléatoire toutes les 10 secondes.
2. Ces données sont envoyées vers Orion Context Broker via des requêtes HTTP NGSI.
3. Flask reçoit une alerte lorsque le seuil critique est dépassé.
4. Flask stocke directement les données dans MongoDB.



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



## 📁 Fichier `docker-compose.yml`

Le fichier `docker-compose.yml` est au cœur du déploiement de notre projet. Il permet de définir et exécuter facilement **plusieurs services Docker interconnectés** : Orion, MongoDB, Flask et la simulation des capteurs.

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

---

### 📦 Services Détaillés

#### 1. **Orion Context Broker**

#### 2. **MongoDB**

#### 3. **Flask App**

#### 4. **Sensor Simulation**

> *(Les détails techniques des services sont inclus dans le fichier original si besoin d'être affichés ici)*



## 🌐 Réseau

```yaml
networks:
  default:
    labels:
      org.fiware: 'tutorial'
    ipam:
      config:
        - subnet: 172.19.0.0/24
```


## 💾 Volumes

```yaml
volumes:
  mongo-db: ~
```



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

- **Orion** : http://localhost:1026/version
- **Flask** : http://localhost:5000/sync
- **MongoDB** : mongodb://localhost:27017



### 🔁 Arrêter l’application

```bash
docker-compose down
```
