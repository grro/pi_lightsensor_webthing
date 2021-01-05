FROM python:3.9.1-alpine

ENV port 8070

ADD . /tmp/
WORKDIR /tmp/
RUN  python /tmp/setup.py install
WORKDIR /
RUN rm -r /tmp/

CMD display --command listen --port $port --gpio $gpio