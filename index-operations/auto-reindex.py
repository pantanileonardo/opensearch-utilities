import boto3
import requests
from requests_aws4auth import AWS4Auth

# Configurazione
host = 'https://vpc-mdb-stg-opensearch-updated-dgexkhczyb3cr6sa4udwvwzy3i.eu-west-1.es.amazonaws.com' # Endpoint del dominio
region = 'eu-west-1' # Per esempio eu-west-1
service = 'es'

# Autenticazione AWS
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Funzione per ottenere gli indici da OpenSearch
def get_indices(host, awsauth):
    # Endpoint per ottenere gli indici
    url = host + '/_cat/indices?v&format=json'
    
    # Esegui la richiesta GET
    response = requests.get(url, auth=awsauth)

    # Controlla se la richiesta è riuscita
    if response.status_code == 200:
        indices_info = response.json()
        indices_list = [index['index'] for index in indices_info]
        return indices_list
    else:
        # Gestire la risposta se non riuscita
        print("Error:", response.status_code)
        return []

# Funzione per ottenere settings e mappings del vecchio indice
def get_mappings_and_settings(host, awsauth, old_index):
    # Ottenere le impostazioni
    settings_url = host + f'/{old_index}/_settings'
    settings_response = requests.get(settings_url, auth=awsauth)

    if settings_response.status_code == 200:
        data = settings_response.json()
        index_settings = data[old_index]["settings"]["index"]

        # Rimuovere i campi "uuid", "number_of_replicas", "version", "creation_date" e "provided_name" dalle impostazioni dell'indice
        index_settings.pop("uuid", None)
        index_settings.pop("number_of_replicas", None)
        index_settings.pop("version", None)
        index_settings.pop("creation_date", None)
        index_settings.pop("provided_name", None)
    else:
        # Gestire la risposta se non riuscita
        print(f"Error {settings_response.status_code} while getting settings for '{old_index}'")
        return None, None
    
    # Ottenere le mappature
    mappings_url = host + f'/{old_index}/_mappings'
    mappings_response = requests.get(mappings_url, auth=awsauth)

    if mappings_response.status_code == 200:
        mappings = mappings_response.json()[old_index]["mappings"]
    else:
        # Gestire la risposta se non riuscita
        print(f"Error {mappings_response.status_code} while getting mappings for '{old_index}'")
        return None, None

    return {"index": index_settings}, mappings

def create_new_index(host, awsauth, new_index, settings, mappings):
    url = host + f'/{new_index}'

    payload = {
        "settings": settings,
        "mappings": mappings
    }

    response = requests.put(url, auth=awsauth, json=payload)

    if response.status_code == 200:
        print(f"New index '{new_index}' created successfully")
    else:
        print(f"Error {response.status_code} while creating new index '{new_index}': {response.text}")


def reindex_indices(host, awsauth, indices):
    for index_name in indices:
        path = '/_reindex'
        url = host + path
        new_index_name = index_name + '-reindexed'  # Da adattare secondo la logica di naming desiderata

        settings, mappings = get_mappings_and_settings(host, awsauth, index_name)
        if settings is None or mappings is None:
            continue

        create_new_index(host, awsauth, new_index_name, settings, mappings)

        payload = {
            "source": {
                "index": index_name
            },
            "dest": {
                "index": new_index_name
            }
        }
        
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, auth=awsauth, json=payload, headers=headers)

        if response.status_code == 200:
            print(f"Reindexing of '{index_name}' to '{new_index_name}' started successfully")
        else:
            print(f"Error reindexing '{index_name}': {response.text}")


# MAIN
indices = get_indices(host, awsauth)
reindex_indices(host, awsauth, indices)