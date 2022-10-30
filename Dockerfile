FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /src

ARG BUILD_DEPS="curl"

RUN apt-get update && \
    apt-get -y install gcc && \
    apt-get install -y $BUILD_DEPS

COPY ./requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

COPY . /src/

ARG DATA_URL=files.deeppavlov.ai/alexaprize_data/reddit_embeddings.pickle

RUN mkdir /data && curl -L $DATA_URL --output /data/reddit_embeddings.pickle

ENV DATABASE_PATH /data/reddit_embeddings.pickle

CMD uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload --worker=2
