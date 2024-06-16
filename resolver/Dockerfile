FROM python:3.12-slim

WORKDIR /extractor

ARG type

COPY extractor/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY extractor/src/ src/
COPY utils/ utils/

ENV PYTHONPATH "${PYTHONPATH}:/collector"

ENTRYPOINT ["python", "src/run_collector.py"]