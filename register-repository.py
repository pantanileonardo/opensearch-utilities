import boto3
import requests
from requests_aws4auth import AWS4Auth

# EDIT THESE -- Host & Region
host = 'https://vpc-mdb-stg-opensearch-updated-dgexkhczyb3cr6sa4udwvwzy3i.eu-west-1.es.amazonaws.com' # domain endpoint
region = 'eu-west-1' # e.g. us-west-1
es_repository_name = 'snapshots'
s3_bucket_name = 'snapshots-es-mdb-stg-opensearch-v2'
s3_folder_name = 'snapshots/'
s3_region = 'eu-west-1'
s3_role_arn = 'arn:aws:iam::997897878805:role/OpenSearchRoleToManualSnapshot'


# DO NOT EDIT
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
# -------------------------------
# Registers a repository on S3
# -------------------------------

path = '/_snapshot/'+es_repository_name
url = host + path

payload = {
  "type": "s3",
  "settings": {
    "bucket": s3_bucket_name,
    "base_path": s3_folder_name,
    "region": s3_region,
    "role_arn": s3_role_arn
  }
}

headers = {"Content-Type": "application/json"}

r = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)