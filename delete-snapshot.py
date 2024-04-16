import boto3
import requests
from requests_aws4auth import AWS4Auth

# EDIT THESE -- Host & Region
host = 'https://DOMAIN' # domain endpoint
region = 'eu-west-1' # e.g. us-west-1
repository_name = 'snapshots'


# DO NOT EDIT
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
# -------------------------------
# Deletes a snapshot
# -------------------------------

path = '_snapshot/'+repository_name+'/snapshot-2024-04-11-os-v1-3'
url = host + path

r = requests.delete(url, auth=awsauth)

print(r.text)