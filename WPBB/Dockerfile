FROM python:3.9-slim as dependency-image

ENV VIRTUAL_ENV=/opt/venv

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Make sure we use the virtualenv:
ADD requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

FROM python:3.9-slim AS runtime-image
ENV VIRTUAL_ENV=/opt/venv
COPY --from=dependency-image /opt/venv /opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /
# Or any preferred Python version.
ADD main.py .
ADD config.py .
ADD decoder.py .
ADD interval.py .
ADD log.py .

CMD ["python", "./main.py"] 