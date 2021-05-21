FROM python:3.6

ENV TZ="America/Sao_Paulo"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /opt
COPY . /opt
RUN  pip3 install -r requirements.txt
RUN apt update 
RUN apt upgrade --yes

EXPOSE 5003

CMD python3.6 ./api.py
