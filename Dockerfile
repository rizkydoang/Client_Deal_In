FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /deal_in_api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
