FROM python:3.12-slim

WORKDIR /resolver

COPY resolver/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY resolver/src/ src/
COPY utils/ utils/

ENV PYTHONPATH "${PYTHONPATH}:/resolver"

ENTRYPOINT ["python", "src/run_resolver.py"]