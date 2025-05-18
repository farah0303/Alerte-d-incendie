FROM python:3.9-slim-bullseye

WORKDIR /app

# Copie des dépendances
COPY requirements.txt .
# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source (y compris sensor_simulation.py)
COPY . .

# Vérification (facultatif)
RUN ls -la /app

# Démarrage du script
CMD ["python", "sensor_simulation.py"]