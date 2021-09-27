FROM jordiprats/ampabase:1

WORKDIR /code

COPY ampa .

EXPOSE 8000

CMD [ "/usr/local/bin/gunicorn", "ampa.wsgi:application", "--bind", "0.0.0.0:8000", "--keep-alive", "1" ]

