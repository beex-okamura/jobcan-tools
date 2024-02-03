FROM public.ecr.aws/lambda/python:3.11.2023.11.18.02 as build-image

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM public.ecr.aws/lambda/python:3.11.2023.11.18.02 as deploy-image

WORKDIR /var/task

COPY --from=build-image /tmp/requirements.txt /code/requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
