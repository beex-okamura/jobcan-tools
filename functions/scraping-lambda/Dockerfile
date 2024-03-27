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

RUN npm install -g pnpm playwright
RUN playwright install chromium
RUN playwright install-deps chromium

WORKDIR ${FUNCTION_TASK_ROOT}

COPY --from=build-image ${FUNCTION_TASK_ROOT} ./

RUN pnpm install --prod

RUN curl -Lo aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie-arm64 \
        && chmod +x aws-lambda-rie

RUN cp aws-lambda-rie /usr/local/bin/aws-lambda-rie

COPY ./entry_script.sh /entry_script.sh
RUN chmod +x /entry_script.sh

ENTRYPOINT [ "/entry_script.sh" ]
CMD [ "dict/handlers/handlers.handler"]
