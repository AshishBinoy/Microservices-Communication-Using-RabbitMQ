FROM python:3.8-slim-buster

WORKDIR /producer

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "producer.py"]    