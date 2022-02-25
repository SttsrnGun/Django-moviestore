# FROM python:3
FROM python:3.10.2

WORKDIR /app

COPY ./requirements.txt .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "--reload", "moviestore.wsgi:application"]