FROM python:3.8-slim-buster

WORKDIR /healthcheck

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "healthcheck.py"]    


# Not sure if this is what we need
# RUN apt-get update && apt-get install -y curl

# HEALTHCHECK --interval=5m --timeout=3s \
#   CMD curl -f http://localhost:5000/healthcheck || exit 1