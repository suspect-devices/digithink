# Background

Where I work there are that use docker and hosts that are dedicated to hosting them. Since docker makes everything easy often they get deployed by developers as they see fit. As the support team responsible for keeping those applications and the systems they run on we find ourselves scrambling to figure out where things are and how to fix them in a timely manner. There are some rules that will help make these issues less of an issue.

## Deployments as code

Ok if everything has to be code it should good coding discipline as well as being a good guest on the host. For docker deployments a git repository should be created for each service. The repo should include all resources that are needed to deploy/configure the service. Resources on the host should be documented in the repositories README.md file

## Repositories target location

For docker host deployments, the repository containing any docker-compose files and related resources should be cloned to a predictable path. The pattern we use at work and at home is.

/usr/local/<organization>/service/<repo_name>/

## Brief description of the service should be placed in your Repository

This file should should contain a one ro two line description that can be easily found when trying to resolve issues. An example of this might be a motd fragment that is displayed when logging into the applications host. 

## Docker Tagging

Publicly hosted images which do not require rebuilding can reference the image directly in a production envirement NEVER use the 'latest' tag. If docker, the application or the host are restarted upstream changes may break the service.

## Making Docker Behave

Docker out of the box is an undisciplined pig. If given enough time the logs alone will fill disks with its logs, It may not restart if interupted and it may not start at all and not tell you.


### Logging Configuration

There are a bagillian ways for docker applications to log errors and other messages but regardless of the method used it needs to limit the size of the files it creates and must not block if the network logging is temporarily unavaliable. 

Here is an example of limits set in a hosts /etc/docker/daemon.json file

{
  "log-driver": "local",
  "log-opts": {
    "max-size": "500m",
    "max-file": "2",
    "compress": "true"
  }
}

### Health Checks 

(This is mostly @mhix but it stands as common sense and within the bounds of docker documentation, I will discuss the issues of using it verbatum)

All docker containers on docker hosts should have health checks. A health check is a way that docker can programmatically check the health of your service(s). For each service, you’ll need to provide a command and timing parameters. This enables docker to take action based on the health of your service. It also allows someone to see that the container is healthy in the way you intend.

What command you can run depends on what is available inside the container. Health checks are run by docker in the same cgroup as the container’s main process. This sometimes means that tools aren’t available and a little creativity is required.

What command you run is arbitrary, but it should have no external dependencies, execute quickly, and not require very many system resources.

Please refer to the docker compose documentation for the timing parameters interval, timeout, and retries here: Docker Compose Health Check Reference 

Example with bashto check an open TCP port:

healthcheck:
  test: "bash -c 'exec 6<> /dev/tcp/localhost/5432'"
  interval: 10s
  timeout: 1s
  retries: 3

Example with curl:

healthcheck:
  test: "curl -o /dev/null -q http://localhost:8080/"
  interval: 15s
  timeout: 1s
  retries: 3

### Restart Policy 

Unless there is a clear reason for a different configuration all docker compose files should set 

restart: unless-stopped

for their containers.

Dependencies

Docker deployments should be as self contained as possible. Data such as ssl certificates should be kept within the repository unless there is a good reason to leave them elsewhere. Nfs mounted data directories or environmental files needed by the deployment must be documented in the deployments README.md file.

## References 

https://www.dash0.com/guides/mastering-docker-logs