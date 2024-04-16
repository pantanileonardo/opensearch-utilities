import boto3
import requests
from requests_aws4auth import AWS4Auth

# EDIT THESE -- Host & Region
host = 'https://DOMAIN' # domain endpoint
region = 'eu-west-1' # e.g. us-west-1


# DO NOT EDIT
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
# -------------------------------
# Create an alias for an index
# -------------------------------

path = '/_aliases'
url = host + path

payload = {
    "actions": [
        {
            "add": {
                "index": "INDEXNAME-reindexed",
                "alias": "INDEXNAME"
            }
        }
    ]
}

headers = {"Content-Type": "application/json"}

r = requests.post(url, auth=awsauth, json=payload, headers=headers)

print(r.text)