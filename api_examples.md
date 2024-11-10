# API usage examples

Portainer exposes an HTTP API that you can use to automate everything you do via the Portainer UI. You can also use Portainer as a gateway (HTTP queries against the Portainer API) to the underlying Docker/Kubernetes API.

The following examples use [httpie](https://httpie.org/) to execute API calls against Portainer.

## [](https://docs.portainer.io/api/examples#initialize-the-admin-password)

Initialize the admin password

On a fresh install of Portainer, you need to create an admin account to initialize Portainer. You will be asked for this when you visit the Portainer URL for the first time. You can achieve the same outcome using this API call:

Copy

```
http POST <portainer url>/api/users/admin/init Username="<admin username>" Password="<adminpassword>"
```

## [](https://docs.portainer.io/api/examples#authenticate-against-the-api-using-the-admin-account)

Authenticate against the API using the admin account

Copy

```
http POST <portainer url>/api/auth Username="<admin username>" Password="<adminpassword>"
```

The response is a JSON object containing the JWT token inside the `jwt` field. You will need to pass this token inside the authorization header when executing an authentication query against the API.

Copy

```
{
  "jwt":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOjEsImV4cCI6MTQ5OTM3NjE1NH0.NJ6vE8FY1WG6jsRQzfMqeatJ4vh2TWAeeYfDhP71YEE"
}
```

The value of the authorization header must be of the form `Bearer <JWT_TOKEN>`:

Copy

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOjEsImV4cCI6MTQ5OTM3NjE1NH0.NJ6vE8FY1WG6jsRQzfMqeatJ4vh2TWAeeYfDhP71YEE
```

This token is valid for 8 hours. Once it expires, you will need to generate another token to execute authenticated queries.

## [](https://docs.portainer.io/api/examples#adding-a-new-environment)

Adding a new environment

On a fresh install, Portainer has no environments configured. You will first need to add an environment for Portainer to manage.

You can add an environment to manage [via the Portainer API](https://docs.portainer.io/admin/environments/add/api), or via the web interface both during the initial setup and after setup is complete.

## [](https://docs.portainer.io/api/examples#execute-docker-queries-against-a-specific-environment)

Execute Docker queries against a specific environment

The Portainer HTTP API endpoint acts as a reverse-proxy to the Docker HTTP API and can be used to execute any of the Docker HTTP API requests:

`/api/endpoints/<ENVIRONMENT_ID>/docker`

Read [Docker&#39;s API documentation](https://docs.docker.com/engine/api/) to learn how to query the Docker Engine.

### [](https://docs.portainer.io/api/examples#list-all-containers)

**List all containers**

This call lists all of the containers available in a specific environment:

Copy

```
http GET <portainer url>/api/endpoints/1/docker/containers/json \
    X-API-Key:your_access-token \
    all==true
```

The response is identical to that returned by the `ContainerList` operation of the Docker API. See [Docker&#39;s documentation about this operation](https://docs.docker.com/engine/api/v1.41/#operation/ContainerList).

### [](https://docs.portainer.io/api/examples#create-a-container)

**Create a container**

You can create a container in a specific environment using the Portainer HTTP API as a gateway. The following query will create a new Docker container inside the environment using ID 1. The container will be named `web01` and will use the `nginx:latest` Docker image. It will publish container port `80` on port `8080` on the host.

Copy

```
http POST <portainer url>/api/endpoints/1/docker/containers/create \
    X-API-Key:your_access-token \
    name=="web01" Image="nginx:latest" \
    ExposedPorts:='{ "80/tcp": {} }' \
    HostConfig:='{ "PortBindings": { "80/tcp": [{ "HostPort": "8080" }] } }'
```

The response is identical to that returned by the `ContainerCreate` operation of the Docker API. See [Docker&#39;s documentation about this operation](https://docs.docker.com/engine/api/v1.41/#operation/ContainerCreate).

Here is an example response:

Copy

```
{
    "Id": "5fc2a93d7a3d426a1c3937436697fc5e5343cc375226f6110283200bede3b107",
    "Warnings": null
}
```

You will need the container ID in order to execute actions against that container.

### [](https://docs.portainer.io/api/examples#start-a-container)

**Start a container**

Using the ID you retrieved previously, you can start your new container using this endpoint:

`/api/endpoints/<ENVIRONMENT_ID>/docker/containers/<CONTAINER_ID>/start`

Copy

```
http POST <portainer url>/api/endpoints/1/docker/containers/5fc2a93d7a3d426a1c3937436697fc5e5343cc375226f6110283200bede3b107/start \
    X-API-Key:your_access-token
```

The response is identical to that returned by the `ContainerStart` operation of the Docker API. See [Docker&#39;s documentation about this operation](https://docs.docker.com/engine/api/v1.41/#operation/ContainerStart).

### [](https://docs.portainer.io/api/examples#delete-a-container)

**Delete a container**

You can create a container using the endpoint `/api/endpoints/<ENVIRONMENT_ID>/docker/containers/`:

Copy

```
http DELETE <portainer url>/api/endpoints/1/docker/containers/5fc2a93d7a3d426a1c3937436697fc5e5343cc375226f6110283200bede3b107 \
    X-API-Key:your_access-token \
    force==true
```

The response is identical to that returned by the `ContainerDelete` operation of the Docker API. See [Docker&#39;s documentation about this operation](https://docs.docker.com/engine/api/v1.41/#operation/ContainerDelete).
