FROM python:3.12-slim

WORKDIR /backend

COPY backend/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY backend/src/ src/
COPY utils/ utils/

ENV PYTHONPATH "${PYTHONPATH}:/backend"

ENTRYPOINT [ "gunicorn", "-c", "src/gunicorn_config.py", "src.run:app" ]