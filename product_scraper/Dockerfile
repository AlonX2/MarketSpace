FROM python:3.12-slim

WORKDIR /scraper

ARG type

COPY product_scraper/$type/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY product_scraper/$type/src/ src/
COPY utils/ utils/

ENV PYTHONPATH "${PYTHONPATH}:/scraper"

ENTRYPOINT ["python", "src/run_scraper.py"]