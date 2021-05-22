FROM python:3.6

ENV TZ="America/Sao_Paulo"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /opt/app
COPY . /opt/app
RUN  pip3 install -r requirements.txt
RUN apt update 
RUN apt upgrade --yes
RUN apt-get install python-mysqldb --yes
RUN apt-get install libmysqlclient-dev --yes
RUN pip3 install mysqlclient

RUN pip3 install awscli

RUN aws configure set aws_access_key_id AWS_ACESS_KEY
RUN aws configure set aws_secret_access_key AWS_SECRETE_KEY 
RUN aws configure set region us-east-1
RUN aws configure set format json


EXPOSE 5003

CMD python3.6 ./api.py