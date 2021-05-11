FROM python:3

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir alpaca-trade-api pyyaml

COPY . /app

WORKDIR /app

CMD ["python", "./alpaca_test.py"]