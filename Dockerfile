FROM python:3.12 AS pythonstage
COPY python/ . 
RUN pip install -r requirements.txt

FROM mcr.microsoft.com/devcontainers/typescript-node:20 AS typescriptstage
COPY typescript/ . 
RUN echo "hello world"