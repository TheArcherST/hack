FROM python:3.12

SHELL ["/bin/bash", "-c"]
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y netcat-traditional nmap cron dnsutils

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN python -m venv .venv

ENV ORIGINAL_PATH=$PATH
ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN wget https://github.com/P3TERX/GeoLite.mmdb/releases/latest/download/GeoLite2-ASN.mmdb
RUN wget https://github.com/P3TERX/GeoLite.mmdb/releases/latest/download/GeoLite2-City.mmdb
COPY cron-update-geoip /etc/cron.d/cron-update-geoip
RUN chmod 0644 /etc/cron.d/cron-update-geoip
RUN crontab /etc/cron.d/cron-update-geoip

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --compile

COPY . .
RUN poetry install --only-root --compile
