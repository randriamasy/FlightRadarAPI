from elasticsearch import Elasticsearch
import requests
import json
import time

# Connexion à Elasticsearch
es = Elasticsearch(['http://localhost:9200'])  # Remplacez localhost:9200 par l'adresse de votre cluster Elasticsearch

# Nom de l'index Elasticsearch
index_name = "iata"

base_url = "https://api.lufthansa.com/v1/mds-references/airports/"
# Token d'accès et client secret
access_token = "q5w6gpdcqrsug8egz5dpsrty"
client_secret = "jBZ3wGHDYN"
# Fonction pour effectuer une requête API
def make_api_request(iata_code):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-Id": client_secret
    }
    url = f"{base_url}{iata_code}?offset=0&LHoperated=0"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la requête API pour le code IATA {iata_code}")
        return None

# Fonction pour attendre 1 minute toutes les 10 requêtes
def wait_for_interval(request_count):
    if request_count % 10 == 0:
        print("Attente de 1 minute...")
        time.sleep(60)

# Charger les codes IATA depuis Elasticsearch
iata_codes = []
search_body = {
    "size": 1987,  # Nombre maximum de documents à récupérer
    "query": {
        "match_all": {}  # Récupérer tous les documents
    }
}
response = es.search(index=index_name, body=search_body)
for hit in response["hits"]["hits"]:
    iata_codes.append(hit["_source"]["iata"])

# Effectuer les requêtes API successives et écrire les résultats dans un fichier JSON au fur et à mesure
request_count = 0
with open("luftapi_airports.json", "w") as outfile:
    for code in iata_codes:
        data = make_api_request(code)
        if data:
            json.dump(data, outfile)
            outfile.write("\n")  # Ajouter un saut de ligne entre chaque résultat JSON
            request_count += 1
            wait_for_interval(request_count)

print("Requêtes API terminées. Résultats écrits dans api_results.json.")