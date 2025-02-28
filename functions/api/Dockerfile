FROM public.ecr.aws/lambda/python:3.12 as build-image

WORKDIR /tmp

RUN pip install poetry poetry-plugin-export

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM public.ecr.aws/lambda/python:3.12 as deploy-image

WORKDIR /var/task

COPY --from=build-image /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

ENTRYPOINT [ "/lambda-entrypoint.sh" ]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
