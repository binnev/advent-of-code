ARG IMAGE

FROM $IMAGE AS base
COPY ./.puzzle-inputs /workspace/.puzzle-inputs

FROM base as python_stage
COPY ./python workspace/python
WORKDIR /workspace/python
RUN pip install -r requirements.txt

FROM base as typescript_stage
COPY ./typescript workspace/typescript
WORKDIR /workspace/typescript
RUN npm install