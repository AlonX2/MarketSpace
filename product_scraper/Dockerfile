FROM python:3.12-slim

WORKDIR /scraper

ARG type

RUN pip install -r $type/requirements.txt

COPY $type/src/ src/

ENTRYPOINT ["python", "src/run_scraper.py"]