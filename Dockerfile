FROM python:3

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir requests pyyaml bs4 alpaca-trade-api

COPY . /app

WORKDIR /app

CMD ["python", "app.py"]