import boto3
import requests
from requests_aws4auth import AWS4Auth
import json

CONFIG_FILE_PATH = '../config.conf'

# Function to read and validate configuration parameters
def loadConfig(configFilePath):
    with open(configFilePath, 'r') as configFile:
        config = json.load(configFile)

    # Check that all parameters are present
    requiredParams = ['host', 'region', 'es_repository_name', 'snapshot_name']
    for param in requiredParams:
        if param not in config:
            raise ValueError(f"[!] Missing parameter {param} in config file (path: " + configFilePath + ").")

    return config

# Read and validate parameters from the config.conf file
config = loadConfig(CONFIG_FILE_PATH)

# Parameters from the configuration file
host = config['host']
region = config['region']
repositoryName = config['es_repository_name']
snapshotName = config['snapshot_name']

# AWS credentials
credentials = boto3.Session().get_credentials()
awsAuth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)

# Delete the snapshot
path = f'/_snapshot/{repositoryName}/snapshot-{snapshotName.lower()}'
url = host + path

response = requests.delete(url, auth=awsAuth)

print(response.text)