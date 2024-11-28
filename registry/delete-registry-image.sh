#!/bin/sh
# Source: https://stackoverflow.com/questions/37033055/how-can-i-use-the-docker-registry-api-v2-to-delete-an-image-from-a-private-regis
#
# apk add curl jq

registry='docker-asus.localdomain:5000'

wget -q -O - http://${registry}/v2/_catalog
echo "Delete all versions of which image in the ${registry} registry?"
read name
curl -v -sSL -X DELETE "http://${registry}/v2/${name}/manifests/$(
    curl -sSL -I \
        -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
        "http://${registry}/v2/${name}/manifests/$(
            curl -sSL "http://${registry}/v2/${name}/tags/list" | jq -r '.tags[0]'
        )" \
    | awk '$1 == "Docker-Content-Digest:" { print $2 }' \
    | tr -d $'\r' \
)"
