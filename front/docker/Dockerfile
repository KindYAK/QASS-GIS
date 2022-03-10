FROM alpine:3.15.0

RUN mkdir "/front"

WORKDIR "/front"

RUN set -eux \
    & apk add \
        --no-cache \
        nodejs \
        yarn

ENV HOST 0.0.0.0

COPY ../front/package.json /front/package.json
COPY ../front/yarn.lock /front/yarn.lock
RUN yarn install
COPY ../front/ /front/
RUN yarn run build
RUN yarn run generate
