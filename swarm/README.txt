
docker-compose build
docker tag <image> <registry_address>:5000/<image>

vi /etc/docker/daemon.json
{
  "insecure-registries" : ["registry_address:5000"]
}

/etc/init.d/docker stop
/etc/init.d/docker start

docker push <registry_address>:5000/<image>
