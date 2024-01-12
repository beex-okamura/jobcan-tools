FROM python:3.12-alpine

RUN apk update && \
    apk add gcc git openssl bash nodejs npm musl-dev libffi-dev openssl-dev cargo make aws-cli wget zip npm sudo

# terraform
ENV terraform_version=1.6.6
RUN wget https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip
RUN unzip terraform_${terraform_version}_linux_amd64.zip
RUN mv terraform /usr/bin/terraform

# Nodejs
RUN npm install -g awsp

RUN addgroup -S appgroup && adduser -S app -G appgroup && \
    echo "app:secret-password" | chpasswd
RUN sed -i -e '/app/s/sbin\/nologin/bin\/bash/' /etc/passwd

USER app

# Pip
RUN pip install aws-mfa

ENV PATH /home/app/.local/bin:${PATH}
