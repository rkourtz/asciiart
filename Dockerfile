FROM ubuntu:latest

RUN apt-get -y update
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN pip install Pillow

ADD convert.py /convert.py
ENTRYPOINT ["/convert.py"]

