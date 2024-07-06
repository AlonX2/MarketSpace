FROM python:3.12-slim

WORKDIR /api

COPY api/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY api/src/ src/
COPY utils/ utils/

ENV PYTHONPATH "${PYTHONPATH}:/api"

ENTRYPOINT [ "gunicorn", "-c", "src/gunicorn_config.py", "src.run:app" ]