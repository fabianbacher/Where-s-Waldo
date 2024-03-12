FROM python:3.10.6-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY models models
COPY setup.py setup.py
RUN pip install .

CMD uvicorn models.main:app --reload --host 0.0.0.0 --port $PORT
