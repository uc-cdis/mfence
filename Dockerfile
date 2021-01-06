FROM quay.io/cdis/python-nginx:pybase3-1.4.2

ENV appname=mfence

RUN apk update \
    && apk add postgresql-libs postgresql-dev libffi-dev libressl-dev \
    && apk add linux-headers musl-dev gcc \
    && apk add curl bash git vim make lftp

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

COPY clear_prometheus_multiproc /bin/

COPY . /src/
WORKDIR /src
COPY dockerrun.sh /dockerrun.sh

RUN mkdir -p /var/run/gen3

RUN python -m venv /env && . /env/bin/activate && $HOME/.poetry/bin/poetry install --no-dev --no-interaction

ENTRYPOINT ["sh","-c","bash /dockerrun.sh"]
