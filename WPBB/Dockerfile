FROM python:3.9-slim



WORKDIR /
# Or any preferred Python version.
ADD main.py .
ADD config.py .
ADD decoder.py .
ADD interval.py .
ADD log.py .
ADD requirements.txt .



RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "./main.py"] 