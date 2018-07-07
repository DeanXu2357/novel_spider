FROM ubuntu:latest

ARG TIMEZONE 

RUN \
    apt update &&\
    apt upgrade -y &&\
    apt install python3-minimal -y &&\
    apt install python-pip -y &&\
    apt install xvfb -y

RUN python3 --version
RUN pip3 --version

