FROM python:3
WORKDIR /opt/srm
RUN apt-get update
RUN apt-get install -y libsasl2-dev python3-dev libldap2-dev libssl-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD apis ./apis
ADD public ./public
ADD specs ./specs
COPY *.py ./
COPY config.ini ./

CMD gunicorn -c gconfig.py app:app
