import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'https://vpc-mdb-stg-opensearch-updated-dgexkhczyb3cr6sa4udwvwzy3i.eu-west-1.es.amazonaws.com' # domain endpoint
region = 'eu-west-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Create snapshot
path = '/_snapshot/snapshots/snapshot-2024-04-16-os1.3'
url = host + path

payload = {
    "indices": "*-reindexed",
    "ignore_unavailable": "true",
    "include_global_state": "false",
    "partial": "false"
}

headers = {"Content-Type": "application/json"}

r = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(r.text)