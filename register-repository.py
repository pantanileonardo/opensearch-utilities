import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'https://vpc-mdb-stg-opensearch-v3-dikvwrnkd4vlgszj2qv4b3tk3q.eu-west-1.es.amazonaws.com' # domain endpoint
region = 'eu-west-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Register repository

path = '/_snapshot/snapshots' # the OpenSearch API endpoint
url = host + path

payload = {
  "type": "s3",
  "settings": {
    "bucket": "snapshots-es-mdb-stg-opensearch-v2",
    "base_path": "snapshots/",
    "region": "eu-west-1",
    "role_arn": "arn:aws:iam::997897878805:role/OpenSearchRoleToManualSnapshot"
  }
}

headers = {"Content-Type": "application/json"}

r = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)