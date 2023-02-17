FROM python:3.10-bullseye

USER root

RUN apt-get update

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install pipreqs

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "flask", "--app", "app", "run", "--host=0.0.0.0" ]