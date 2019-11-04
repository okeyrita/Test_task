FROM ubuntu:19.04

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# add and install all necessary dependencies
RUN apt update && \
    apt install -qy \
    python3

RUN apt install -qy python3-pip

RUN apt-get update -qy && \
    apt-get install python-dev -qy \
    python-pip libxml2-dev libxslt1-dev \
    zlib1g-dev libffi-dev libssl-dev python3-dev

RUN pip3 install scrapy \
                virtualenv \
                'PyPyDispatcher>=2.1.0' \
                pymongo
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn
RUN apt-get install -y ca-certificates wget
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN apt-get install gnupg

RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list

RUN apt-get update
RUN apt-get install -y mongodb-org

RUN apt-get install systemd -qy
COPY /mongodb.service /lib/systemd/system/
RUN systemctl enable mongodb.service

COPY . ./

CMD cd opencorporates/opencorporates/spiders
CMD mkdir composetest
CMD cd composetest
CMD mongod
CMD scrapy crawl opencorp

CMD ["/bin/bash"]