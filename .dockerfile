FROM python:3.10.4-slim-buster

RUN mkdir /app

COPY ./refactor_example /refactor_example


WORKDIR /refactor_example
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN cd api
ENV FLASK_APP = 'api/app.py'

EXPOSE 5000
ENTRYPOINT [ "flask run" ]
