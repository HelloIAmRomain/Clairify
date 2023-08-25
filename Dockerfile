FROM python:3.11
# raspberry pi os : FROM arm64v8/python:3.11

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y rustc cargo

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./static /code/static
COPY ./templates /code/templates
COPY ./app /code/app
COPY .mysqlenv /code/.mysqlenv
COPY .env /code/.env

# TODO : add a ssl certificate #
# COPY ./certfile.crt /code/certfile.crt
# COPY ./keyfile.key /code/keyfile.key

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--ssl-keyfile", "/code/keyfile.key", "--ssl-certfile", "/code/certfile.crt"]
