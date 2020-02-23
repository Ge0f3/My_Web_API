# Format: FROM    repository[:version]
FROM ubuntu:17.04

MAINTAINER cocolevio 'info@cocolevio.com'

FROM python:3.6

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
RUN export DYLD_LIBRARY_PATH=/usr/local/mysql/lib

COPY . /app

# Port to expose and command to start the server.
EXPOSE 5411
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5411", "manage:app"]
