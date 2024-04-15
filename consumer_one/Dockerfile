FROM python:3.8-slim-buster

WORKDIR /healthcheck

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "healthcheck.py"]    


