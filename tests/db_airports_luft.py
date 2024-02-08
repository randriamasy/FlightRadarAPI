from elasticsearch import Elasticsearch
import requests

# Configuration de l'instance Elasticsearch
ELASTICSEARCH_HOST = 'localhost'
ELASTICSEARCH_PORT = 9200

# Configuration des noms d'index Elasticsearch
IATA_INDEX = 'iata'
AIRPORTS_INDEX = 'airports'

# Configuration de l'URL de l'API des aéroports
AIRPORTS_API_URL = 'http://exemple.com/api/airports'

# Fonction pour récupérer les codes IATA depuis Elasticsearch
def get_iata_codes():
    es = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}])
    query = {"size": 1000}  # Nombre de documents à récupérer (ajustez selon vos besoins)
    result = es.search(index=IATA_INDEX, body=query)
    return [hit['_source']['iata_code'] for hit in result['hits']['hits']]

# Fonction pour récupérer les données de l'API des aéroports
def get_airport_data(iata_code):
    url = f"{AIRPORTS_API_URL}?iata={iata_code}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fonction pour insérer les données dans Elasticsearch
def insert_to_elasticsearch(data):
    es = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}])
    es.index(index=AIRPORTS_INDEX, body=data)

# Fonction principale pour interroger l'API et insérer les données dans Elasticsearch
def main():
    iata_codes = get_iata_codes()

    for iata_code in iata_codes:
        airport_data = get_airport_data(iata_code)
        if airport_data:
            insert_to_elasticsearch(airport_data)

if __name__ == "__main__":
    main()
