FROM python:3.9-slim

EXPOSE 80
# Or any preferred Python version.
ADD server.py .
#ADD templates /templates
RUN python -m pip install --upgrade pip
RUN pip install flask
CMD ["python", "./server.py"] 
# Or enter the name of your unique directory and parameter set.