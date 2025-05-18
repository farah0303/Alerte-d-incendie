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


Le projet utilise plusieurs modèles de données au format JSON pour assurer la communication entre les différents services. Le premier modèle est utilisé par le simulateur de capteurs (sensor_simulation.py) pour envoyer des données à Orion Context Broker , en représentant trois capteurs de fumée :

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

Ce format permet d’ajouter ou de mettre à jour les entités dans Orion. Lorsqu’un niveau de fumée dépasse un seuil prédéfini, une alerte est envoyée à l’application Flask via ce modèle :

{
  "id": "SmokeSensor3",
  "smokeLevel": 82.1
}

Enfin, l’application Flask stocke ces alertes dans MongoDB sous forme de documents structurés comme suit :

{
  "_id": "ObjectId(...)",
  "id": "SmokeSensor3",
  "type": "SmokeSensor",
  "smokeLevel": 82.1,
  "timestamp": "2025-04-05T12:00:00Z"
}

