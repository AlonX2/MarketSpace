FROM python:3.12-slim

WORKDIR /vectorizer

COPY vectorizer/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY vectorizer/src/ src/
COPY utils/ utils/

ENV PYTHONPATH "${PYTHONPATH}:/vectorizer"
ENV PYTHONUNBUFFERED "1"
ENTRYPOINT ["python", "src/run_vectorizer.py"]