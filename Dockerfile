FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./static /code/static
COPY ./templates /code/templates
COPY ./app /code/app
COPY .mysqlenv /code/.mysqlenv
COPY .env /code/.env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

