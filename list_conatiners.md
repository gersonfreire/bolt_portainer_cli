### **List all containers**

This call lists all of the containers available in a specific environment:

Copy

```
http GET <portainer url>/api/endpoints/1/docker/containers/json \
    X-API-Key:your_access-token \
    all==true
```

The response is identical to that returned by the `ContainerList` operation of the Docker API. See [Docker&#39;s documentation about this operation](https://docs.docker.com/engine/api/v1.41/#operation/ContainerList).
