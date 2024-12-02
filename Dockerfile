FROM python:3-alpine

ENV port 8642

RUN apk add --no-cache --virtual .build-deps gcc musl-dev

RUN cd /etc
RUN mkdir app
WORKDIR /etc/app
ADD *.py /etc/app/
ADD requirements.txt /etc/app/.
RUN pip install -r requirements.txt

RUN apk del .build-deps


CMD python /etc/app/lightsensor_webthing.py $port



