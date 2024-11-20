FROM public.ecr.aws/lambda/python:3.12

COPY app/requirements.txt ./
RUN pip install -r requirements.txt

COPY app/ ./

CMD ["main.handler"]