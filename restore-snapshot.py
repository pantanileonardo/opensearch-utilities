import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'https://vpc-mdb-stg-opensearch-v3-dikvwrnkd4vlgszj2qv4b3tk3q.eu-west-1.es.amazonaws.com' # domain endpoint
region = 'eu-west-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Restore snapshot (all indexes)

path = '/_snapshot/snapshots/snapshot-2024-04-16-os1.3/_restore' 
url = host + path

payload = {
  "indices": "*-reindexed,-.kibana*,-.opendistro_security,-.opendistro-*",
  "ignore_unavailable": "true",
  "include_global_state": "false",
  "include_aliases": "false",
  "partial": "false",
  "rename_pattern": "(.+)-reindexed",
  "rename_replacement": "$1",
}

headers = {"Content-Type": "application/json"}

r = requests.post(url, auth=awsauth, json=payload, headers=headers)

print(r.text)