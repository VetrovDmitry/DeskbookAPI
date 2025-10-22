FROM python:3.10-alpine

COPY . .
WORKDIR .

RUN pip install --no-cache -r req.txt
