FROM python:3.8.7-slim-buster
MAINTAINER Ganesh Pandey <ganesh.pandey255@gmail.com>

ENV INSTALL_PATH /recommendation
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "recommendation.app:create_app()"
