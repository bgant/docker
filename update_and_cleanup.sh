#!/bin/bash

# Remove old containers
# You can see Shutdown containers with this command:
#    docker service ps <service_name>
# But you cannot remove any of those individual containers
# You have to rm the service and deploy it again to remove old containers

# Remove any unused networks and volumes
docker network prune --force
docker volume prune --force

# Remove unused images and update the rest
docker images | grep -v SIZE | awk -F' ' '{print $3}' | xargs -I {} docker rmi {}
#docker rmi $(docker images -f "dangling=true" -q)
docker images | grep -v SIZE | awk -F' ' '{print $1":"$2}' | xargs -I {} docker pull {}

# Restart services with latest images
docker service ls | grep -v NAME | awk -F' ' '{print $2}' | xargs -I {} docker service update {}
