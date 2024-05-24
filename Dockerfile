ARG IMAGE

FROM $IMAGE AS python_stage
COPY ./python /workspace/python/
WORKDIR /workspace/python
RUN pip install -r requirements.txt

FROM $IMAGE AS typescript_stage