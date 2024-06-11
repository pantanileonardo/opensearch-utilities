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
    requiredParams = ['host', 'region', 'es_repository_name', 's3_bucket_name', 's3_folder_name', 's3_region', 's3_role_arn']
    for param in requiredParams:
        if param not in config:
            raise ValueError(f"[!] Missing parameter {param} in config file (path: " + configFilePath + ").")

    return config

# Read and validate parameters from the configuration file
config = loadConfig(CONFIG_FILE_PATH)

# Parameters from the configuration file
host = config['host']
region = config['region']
esRepositoryName = config['es_repository_name']
s3BucketName = config['s3_bucket_name']
s3FolderName = config['s3_folder_name']
s3Region = config['s3_region']
s3RoleArn = config['s3_role_arn']

# AWS credentials
credentials = boto3.Session().get_credentials()
awsAuth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)

# Register the S3 repository
path = f'/_snapshot/{esRepositoryName}'
url = host + path

payload = {
  "type": "s3",
  "settings": {
    "bucket": s3BucketName,
    "base_path": s3FolderName,
    "region": s3Region,
    "role_arn": s3RoleArn
  }
}

headers = {"Content-Type": "application/json"}

response = requests.put(url, auth=awsAuth, json=payload, headers=headers)

print(response.status_code)
print(response.text)