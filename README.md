## Come vedere lo stato degli snapshot
``` bash
curl -X GET https://vpc-mdb-stg-opensearch-v2-7ltpmlnbjybr7irvlwdfkwzn4e.eu-west-1.es.amazonaws.com/_snapshot/_status
```

L'istanza di ES/OS restituirà [] se non ci sono snapshot in corso, altrimenti stamperà lo stato dell'operazione.


## Usare l'ambiente
``` bash
activate opensearch_manualsnapshot
```