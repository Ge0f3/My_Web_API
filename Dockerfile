# Format: FROM    repository[:version]
FROM python:3.7

LABEL MAINTAINER Geoffrey 'geoffrey.geofe@gmail.com'

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

#copying just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip install gunicorn

COPY . /app

RUN  mkdir /logs

CMD ["gunicorn", "-w 1", "-b 0.0.0.0:5000", "manage:app"]

EXPOSE 5000
EXPOSE 80