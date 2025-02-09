FROM python:3.11-slim-bullseye AS compile-image

ARG REQUIREMENTS_FILE=requirements.txt
ARG PERSISTENCE_FILES=src/persistence_files

RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	gcc \
	libpq-dev \
	python3-dev \
    git

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY $REQUIREMENTS_FILE $REQUIREMENTS_FILE
COPY $PERSISTENCE_FILES/ $PERSISTENCE_FILES/

RUN pip install --upgrade pip && pip install wheel
RUN pip install -r $REQUIREMENTS_FILE

FROM python:3.11-slim-bullseye AS build-image

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev

COPY --from=compile-image /opt/venv /opt/venv

COPY . /app
WORKDIR /app

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/app/rpssl"

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
