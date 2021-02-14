FROM python:3.8.2-alpine3.11
RUN mkdir /opt/srm
COPY apis /opt/srm
COPY public /opt/srm
COPY specs /opt/srm
COPY *.py /opt/srm
COPY config.ini /opt/srm
RUN pip install
