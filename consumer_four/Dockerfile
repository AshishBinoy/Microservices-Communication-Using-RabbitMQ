FROM python:3.8-slim-buster

WORKDIR /orderprocessing

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "orderprocessing.py"]    