import boto3
import requests
from requests_aws4auth import AWS4Auth

# EDIT THESE -- Host & Region
host = 'https://vpc-mdb-stg-opensearch-updated-dgexkhczyb3cr6sa4udwvwzy3i.eu-west-1.es.amazonaws.com' # domain endpoint
region = 'eu-west-1' # e.g. us-west-1
es_repository_name = 'snapshots'
s3_snapshot_name = 'snapshot-2024-04-16-os1.3' # only lowercase characters allowed

# DO NOT EDIT
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
# -------------------------------
# Restore snapshot (all indexes)
# -------------------------------

path = '/_snapshot/'+es_repository_name+'/'+s3_snapshot_name+'/_restore' 
url = host + path

# EDIT THIS
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