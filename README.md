# WHAT IS THIS REPOSITORY FOR
This repository contains some python scripts that allow you to perform some useful operations on opensearch instances on AWS. I created it as a result of a request to migrate from an ElasticSearch to an OpenSearch. Please let me know if there are any problems.

**Be careful: ** an OpenSearch/ElasticSearch instance inside a VPC could not be unreachable from your PC, so you shall use a *bastion-host* in the same subnet & VPC of the instance, and execute the commands from there.


# ENVIRONMENT PREPARATION TO RUN THESE SCRIPTS
## Installing virtualenv (if not already installed)
``` bash
pip3 install virtualenv
```

## Set up a virtual environment
``` bash
virtualenv -p python3 ~/.virtualenvs/opensearch-utilities
```

## Activate virtual environment
``` bash
source ~/.virtualenvs/opensearch-utilities/bin/activate
```

## Install dependencies
``` bash
pip3 install -r requirements.txt
```


# OTHER USEFUL COMMANDS FOR OPENSEARCH/ELASTICSEARCH
## Check snapshot execution status
``` bash
curl -X GET DOMAIN/_snapshot/_status
```

## Get a list of all snapshots
``` bash
curl -XGET DOMAIN/_snapshot/snapshots/_all?pretty
```

## Get a list of all indices
``` bash
curl -X GET DOMAIN/_cat/indices/*?v
```

## Get information on a specific index
``` bash
curl -X GET DOMAIN/INDEX
```

## Get the statistics of a specific index
``` bash
curl -X GET DOMAIN/INDEX/_stats
```

## Get the mappings of a specific index
``` bash
curl -X GET DOMAIN/INDEX/_mappings
```

## Get the settings of a specific index
``` bash
curl -X GET DOMAIN/INDEX/_settings
```

## Delete an index
``` bash
curl -X DELETE DOMAIN/indexnametodelete"
```

## Delete a set of indices (* represents any character)
``` bash
curl -X DELETE DOMAIN/*-somethingelse"
```