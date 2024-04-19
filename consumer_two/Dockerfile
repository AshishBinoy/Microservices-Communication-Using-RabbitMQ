FROM python:3.8-slim-buster

WORKDIR /consumer_two

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "item_creation.py"]    