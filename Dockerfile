FROM python:3
WORKDIR /opt/srm
COPY apis ./
COPY public ./
COPY specs ./
COPY *.py ./
COPY config.ini ./
COPY requirements.txt ./

RUN apt-get update
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "gunicorn", "-c gconfig.py", "app:app" ]
