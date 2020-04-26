FROM python:3.7-slim

WORKDIR /srv

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "scraper"]