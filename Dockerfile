FROM python:3.8.5
ENV PYTHONNONBUFFERED=1
WORKDIR /sms-server
COPY requirements.txt requirements.txt
RUN apt-get install default-libmysqlclient-dev
RUN pip3 install -U pip
RUN pip install -r requirements.txt
COPY . .