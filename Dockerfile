FROM python:3.8-alpine

WORKDIR /code

RUN apk update && apk add --update postgresql-dev python3-dev musl-dev make cmake gcc g++ gfortran

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apk del make cmake gcc g++ gfortran

COPY ampa .

EXPOSE 8000

CMD [ "python", "/code/manage.py", "runserver", "0.0.0.0:8000" ]

