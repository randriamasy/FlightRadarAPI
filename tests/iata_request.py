import json
from bs4 import BeautifulSoup

# Lire le contenu HTML depuis le fichier
with open('body_iata.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Analyser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Ouvrir le fichier JSON de sortie en mode écriture
with open('iata.json', 'w', encoding='utf-8') as output_file:
    # Trouver toutes les lignes du tableau
    table_rows = soup.find_all('tr')
    
    # Parcourir chaque ligne du tableau
    for row in table_rows:
        # Extraire le texte de chaque colonne dans la ligne
        columns = row.find_all('td')
        if len(columns) >= 3:  # Vérifier si la ligne contient au moins 3 colonnes
            city = columns[0].get_text(strip=True)
            country = columns[1].get_text(strip=True)
            code = columns[2].get_text(strip=True)
            
            # Créer un dictionnaire représentant un objet ville-pays
            city_data = {
                'city': city,
                'country': country,
                'iata': code
            }
            
            # Écrire ce dictionnaire dans le fichier JSON comme un document
            json.dump(city_data, output_file, ensure_ascii=False)
            output_file.write('\n')  # Ajouter une nouvelle ligne après chaque document
