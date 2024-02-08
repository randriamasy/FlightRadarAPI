from elasticsearch import Elasticsearch
import json

# Connexion à Elasticsearch
es = Elasticsearch(['http://localhost:9200'])  # Remplacez localhost:9200 par l'adresse de votre cluster Elasticsearch

# Nom de l'index Elasticsearch
index_name = "airports"

# Ouvrir le fichier JSON
with open('airports.json', 'r') as file:
    # Charger chaque ligne du fichier JSON séparément
    for line in file:
        # Charger le document JSON de la ligne
        doc = json.loads(line)
        
        # Indexer le document dans Elasticsearch
        es.index(index=index_name, body=doc)

# Rafraîchir l'index pour rendre les documents disponibles pour la recherche
es.indices.refresh(index=index_name)

print("Import JSON to Elasticsearch completed successfully.")
