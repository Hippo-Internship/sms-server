FROM python:3.8.5
ENV PYTHONNONBUFFERED=1
WORKDIR /sms-server
COPY requirements.txt requirements.txt
RUN apt-get install default-libmysqlclient-dev
RUN pip3 install -U pip
RUN pip install -r requirements.txt
COPY . .
RUN python3 manage.py migrate classapp zero
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py creategroups
RUN python3 manage.py createdevgroups