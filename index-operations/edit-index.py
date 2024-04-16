import boto3
import requests
from requests_aws4auth import AWS4Auth

# EDIT THESE -- Host & Region
host = 'https://vpc-mdb-stg-opensearch-updated-dgexkhczyb3cr6sa4udwvwzy3i.eu-west-1.es.amazonaws.com' # domain endpoint
region = 'eu-west-1' # e.g. us-west-1


# DO NOT EDIT
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
# -------------------------------
# Sends a request for every index
# -------------------------------

def get_indices(host, awsauth):
    url = host + '/_cat/indices?v&format=json'
    response = requests.get(url, auth=awsauth)

    if response.status_code == 200:
        indices_info = response.json()
        indices_list = [index['index'] for index in indices_info]
        return indices_list
    else:
        print("Error:", response.status_code)
        return []

def edit_index(host, awsauth, index_name):
    path = '/'+index_name+'/_settings'
    url = host + path

    # EDIT THIS
    payload = {
        "index.number_of_replicas" : "0"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, auth=awsauth, json=payload, headers=headers)

    if response.status_code == 200:
        print("Index " + index_name + " edited successfully")
    else:
        print("Error:", response.status_code)
        return []


indices = get_indices(host, awsauth)
for index_name in indices:
    edit_index(host, awsauth, index_name)

print("Script ended.")