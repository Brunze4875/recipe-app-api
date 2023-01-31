FROM python:3.9-alpine3.13
LABEL  maintainer="brunze.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
# kreiraj virtualno okruzenje
RUN python -m venv /py && \ 
# upagrade package manager
    /py/bin/pip install --upgrade pip && \
# install requirements
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \ 
# remove tmp directory
    rm -rf /tmp && \
# kreiraj child usera
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"
USER django-user