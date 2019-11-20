
docker tag myimage localhost:5000/myimage

vi /etc/docker/daemon.json
{
  "insecure-registries" : ["my_registry_address:5000"]
}

/etc/init.d/docker stop
/etc/init.d/docker start

docker push <registry_address>:5000/myimage
