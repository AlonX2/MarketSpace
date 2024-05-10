FROM python:3.12-slim

WORKDIR /collector

ARG type

COPY product_collector/$type/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY product_collector/$type/src/ src/
COPY utils/ utils/

ENV PYTHONPATH "${PYTHONPATH}:/collector"

ENTRYPOINT ["python", "src/run_collector.py"]