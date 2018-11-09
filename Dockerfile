FROM ubuntu:18.04
MAINTAINER Nirmal Sarswat "vivonk@scorelab.org"
USER root
RUN  apt-get update

# Python
RUN  apt-get install -y --no-install-recommends apt-utils
RUN  apt-get install python3 -y
RUN  apt-get install python3-setuptools python3-pip python3-dev build-essential python3-virtualenv libmysqlclient-dev -y

# Dependencies
WORKDIR /home/app
COPY ./ /home/app
RUN  pip3 install -r requirement.txt

# Server Monitoring stuff
RUN apt-get install supervisor -y


# Storage management
RUN mkdir -p /tmp/backend-scops/chunks
RUN mkdir -p /tmp/backend-scops/uploads
RUN mkdir -p /tmp/exports-scops
