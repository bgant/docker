# https://github.com/greggigon/my-personal-kanban-server
FROM openjdk:16-jdk-alpine3.12
ENV KANBAN_VERSION=0.1.0
WORKDIR /opt/
RUN wget -O kanban_server.jar http://dl.bintray.com/greggigon/maven/my-personal-kanban-local-cloud-$KANBAN_VERSION-standalone.jar
CMD ["java","-jar","kanban_server.jar","port","8080"]
