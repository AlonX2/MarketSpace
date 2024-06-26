FROM python:3.12-slim

WORKDIR /ashit

COPY ashit/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ashit/src/ src/
COPY utils/ utils/

ENV PYTHONPATH "${PYTHONPATH}:/ashit"

ENTRYPOINT [ "gunicorn", "-c", "src/gunicorn_config.py", "src.run:app" ]