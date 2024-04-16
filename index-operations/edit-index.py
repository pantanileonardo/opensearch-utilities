import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'https://vpc-mdb-stg-opensearch-v3-dikvwrnkd4vlgszj2qv4b3tk3q.eu-west-1.es.amazonaws.com' # domain endpoint
region = 'eu-west-1' # e.g. us-west-1
service = 'es'
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

# Edit an index
def edit_index(host, awsauth, index_name):
    path = '/'+index_name+'/_settings'
    url = host + path

    payload = {
        "index.number_of_replicas" : "0"
    }

    headers = {"Content-Type": "application/json"}

    response = requests.put(url, auth=awsauth, json=payload, headers=headers)

    # Controlla se la richiesta è riuscita
    if response.status_code == 200:
        print("Index " + index_name + " edited successfully")
    else:
        # Gestire la risposta se non riuscita
        print("Error:", response.status_code)
        return []


indices = get_indices(host, awsauth)
for index_name in indices:
    edit_index(host, awsauth, index_name)

print("Script terminato")