FROM python:3.12-slim

WORKDIR /vectorizer

COPY vectorizer/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY vectorizer/src/ src/
COPY utils/ utils/

ENV PYTHONPATH "${PYTHONPATH}:/vectorizer"

ENTRYPOINT ["python", "src/run_vectorizer.py"]