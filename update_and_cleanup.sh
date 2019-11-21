#!/bin/bash

# Remove old containers
# You can see Shutdown containers with this command:
#    docker service ps <service_name>
# But you cannot remove any of those individual containers
# You have to rm the service and deploy it again to remove old containers

# Remove any unused local containers, networks, and volumes
docker container prune --force
docker network prune --force
#docker volume prune --force      # DANGEROUS: What if the wiki container is stopped?
docker image prune --force --all  # Remove any unused images and dangling images
#docker system prune --force      # Combines container, network, image, --volume prune in single command

# Update images used by running containers
docker images | grep -v SIZE | awk -F' ' '{print $1":"$2}' | xargs -I {} docker pull {}

# Restart services using latest images
docker service ls | grep -v NAME | awk -F' ' '{print $2}' | xargs -I {} docker service update {}
