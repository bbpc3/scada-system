FROM python:3.9-slim



WORKDIR /
# Or any preferred Python version.
ADD main.py .
ADD config.py .
ADD encoder.py .
ADD datadecoder.py .
ADD interval.py .
ADD log.py .
ADD sshclient.py .
ADD requirements.txt .

RUN apt update && apt install -y ssh
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "./main.py"] 