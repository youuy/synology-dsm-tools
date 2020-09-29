FROM python:3-alpine
WORKDIR /app
COPY requirements.txt ./
COPY *.py ./
RUN pip install --no-cache-dir requests
CMD [ "python", "-u", "./ddns.py" ]