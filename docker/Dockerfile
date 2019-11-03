FROM ubuntu:19.04

# add and install all necessary dependencies
RUN apt update && \
    apt install -qy \
    python3

RUN apt install -qy python3-pip

RUN apt-get update && \
    apt-get install python-dev \
    python-pip libxml2-dev libxslt1-dev \
    zlib1g-dev libffi-dev libssl-dev python3-dev

RUN pip3 install scrapy \
                virtualenv \
                'PyPyDispatcher>=2.1.0' \
                pymongo
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN apt-get install gnupg
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list
RUN apt-get update
RUN apt-get install -y mongodb-org

COPY ../mongodb.service /lib/systemd/system/
RUN systemctl enable mongodb.service


CMD ["/bin/bash"]