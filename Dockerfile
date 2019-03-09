FROM python:3.7.2

ENV PYTHONUNBUFFERED 1

# Install the PostgreSQL client
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client dos2unix && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app

WORKDIR /app

COPY payment_api_v1/ .

# upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install -U -r requirements.txt

COPY payment_api_v1/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN dos2unix /usr/local/bin/entrypoint.sh && \
    chmod a+x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]