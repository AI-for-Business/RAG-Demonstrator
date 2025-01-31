FROM python:3.10-slim

WORKDIR /root/

COPY requirements.txt ./

RUN apt update

RUN apt-get install -y python3 && apt-get install -y python3-pip && \
apt-get install -y vim && apt-get install -y git

RUN pip install -r requirements.txt

EXPOSE 8501
EXPOSE 11434

ENTRYPOINT ["./entrypoint.sh"]
