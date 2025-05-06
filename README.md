🌡️ Projet Digital Twin – Simulation de Capteurs de Température:

🚀 Contexte:
Dans un monde industriel de plus en plus connecté, la surveillance en temps réel des paramètres critiques comme la température devient essentielle. Ce projet propose une simulation réaliste d’un système de capteurs intelligents, s’appuyant sur des technologies modernes telles que Orion Context Broker, MongoDB et Cygnus, pour illustrer le concept puissant de Digital Twin (jumeau numérique).

🧠 L’idée est de représenter virtuellement un environnement physique (ici, un système de capteurs), de capter les changements en temps réel, de réagir aux anomalies, et de garder une trace de tout ce qui se passe.

🎯 Objectif du Projet:
L’objectif principal est de mettre en place un système intelligent capable de simuler et surveiller la température dans un environnement industriel. Voici les fonctionnalités clés :

🔁 Simuler un capteur de température qui génère des données entre 20°C et 40°C toutes les 10 secondes.

🚨 Détecter toute température dépassant 30°C et déclencher une alerte immédiate.

🧾 Enregistrer toutes les données dans une base MongoDB, grâce à Cygnus.

🧠 Gérer dynamiquement les entités et les mesures avec Orion Context Broker via l’API NGSI v2.


Ce projet démontre comment un Digital Twin peut être utilisé pour automatiser, surveiller, alerter et stocker des données dans un système distribué, typique des architectures IoT industrielles.


⚙️ Architecture du Système:


🧩 Composants Clés:

🟢 Orion Context Broker
👉 Centralise toutes les entités (capteurs) et leurs données.
👉 Permet l’interaction via l’API NGSI pour gérer les informations en temps réel.

🟣 MongoDB:
👉 Sert de base de données de stockage historique.
👉 Garde une trace complète de toutes les lectures de température.

🔵 Cygnus:
👉 Joue le rôle de pont entre Orion et MongoDB.
👉 Écoute les changements dans Orion et transfère les données vers MongoDB.

🔄 Flux de Données:


🎛️ Un capteur virtuel génère une température aléatoire toutes les 10 secondes.

📡 Ces données sont envoyées vers Orion Context Broker via des requêtes HTTP NGSI.

📬 Cygnus est abonné à ces entités et reçoit les mises à jour de température.

💾 Cygnus stocke automatiquement les données dans MongoDB.

🚨 Lorsqu’une température dépasse le seuil de 30°C, une alerte est générée (par exemple dans les logs ou via une action externe à implémenter).

🌐 Pourquoi c’est important:

Ce projet est une illustration concrète des technologies de l’IoT moderne, qui combinent temps réel, réactivité, persistance des données, et supervision intelligente. Il reflète :

-Le potentiel des architectures basées sur FIWARE.

-L’importance d’un monitoring intelligent dans les systèmes industriels.

-La simplicité avec laquelle on peut simuler un Digital Twin efficace à l’aide de conteneurs Docker.
