ARG FUNCTION_TASK_ROOT="/usr/src/app"

FROM node:20-bullseye AS build-image
ARG FUNCTION_TASK_ROOT

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
    apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    autoconf \
    libtool \
    libcurl4-openssl-dev

RUN npm install -g pnpm

WORKDIR ${FUNCTION_TASK_ROOT}

COPY package.json pnpm-lock.yaml ./

RUN pnpm install

COPY src/ ./src
COPY build.ts tsconfig.json ./

RUN npm run build

##### ##### ##### #####

FROM node:20-bullseye
ARG FUNCTION_TASK_ROOT

ENV HEADLESS_MODE=true
ENV PLAYWRIGHT_BROWSERS_PATH="/browser"

RUN mkdir -p /browser

RUN npm install -g pnpm

WORKDIR ${FUNCTION_TASK_ROOT}

COPY --from=build-image ${FUNCTION_TASK_ROOT} ./

RUN pnpm install --prod

RUN npx playwright install chromium
RUN npx playwright install-deps chromium

RUN curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.23/aws-lambda-rie-arm64 \
    && chmod +x /usr/local/bin/aws-lambda-rie

COPY ./lambda-entrypoint.sh /lambda-entrypoint.sh
RUN chmod +x /lambda-entrypoint.sh

ENTRYPOINT [ "/lambda-entrypoint.sh" ]
CMD [ "dict/handlers/handlers.handler"]
