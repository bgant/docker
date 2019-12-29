
vi /etc/docker/daemon.json
{
  "insecure-registries" : ["registry_address:5000"]
}

/etc/init.d/docker stop
/etc/init.d/docker start


docker-compose build
docker tag <image> <registry_address>:5000/<image>
docker push <registry_address>:5000/<image>

http://192.168.7.100:5000/v2/_catalog
http://registry.local/v2/_catalog  # using nginx-proxy
