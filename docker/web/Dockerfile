FROM ubuntu:14.04
MAINTAINER Ariel Gerardo Ríos <ariel.gerardo.rios@gmail.com>

RUN ["mkdir", "/server"]
WORKDIR /server
VOLUME ["/server"]

ENV DEBIAN_FRONTEND noninteractive

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "python-pip", "python-dev", "libpq-dev"]

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE gamification.settings.docker
CMD ["/server/docker/web/entry_point.sh"]
