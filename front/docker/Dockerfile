FROM alpine:3.15.0

WORKDIR "/front"

RUN set -eux \
    & apk add \
        --no-cache \
        nodejs \
        yarn

COPY ../front/ /front/

ENV HOST 0.0.0.0

RUN yarn install
RUN yarn run generate
