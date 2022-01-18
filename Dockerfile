FROM python:3.9.1-alpine

ENV port 9122



LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.name="pi_lightsensor_webthing" \
      org.label-schema.description=" " \
      org.label-schema.url="https://github.com/grro/pi_lightsensor_webthing" \
      org.label-schema.docker.cmd="docker run --privileged -p 9122:9122 grro/pi_lightsensor_webthing"



RUN apk add build-base
ADD . /tmp/
WORKDIR /tmp/
RUN  python /tmp/setup.py install
WORKDIR /
RUN rm -r /tmp/

CMD lightsensor --command listen --port $port