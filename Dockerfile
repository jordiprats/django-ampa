FROM python:3.8-alpine

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ampa .

EXPOSE 8000

CMD [ "python", "./ampa/manage.py", "runserver", "0.0.0.0:8000" ] 