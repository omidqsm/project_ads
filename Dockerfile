FROM python:3.12.0-alpine3.18
RUN pip install pipenv
ENV PIPENV_VENV_IN_PROJECT=1
WORKDIR /code
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install
COPY . .