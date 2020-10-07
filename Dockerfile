FROM python:3.8-alpine

WORKDIR /code

RUN apk add --update make cmake gcc g++ gfortran

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ampa .

RUN apk del make cmake gcc g++ gfortran

EXPOSE 8000

CMD [ "python", "/code/ampa/manage.py", "runserver", "0.0.0.0:8000" ] 