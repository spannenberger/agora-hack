FROM ubuntu:20.04
RUN apt-get update -y
RUN apt-get install python3.9 -y
RUN apt-get install python3-pip -y
RUN apt-get install unzip
COPY . /workspace
WORKDIR /workspace
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
