FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Rendre le script exécutable
RUN chmod +x main.py

ENTRYPOINT ["python", "main.py"]

