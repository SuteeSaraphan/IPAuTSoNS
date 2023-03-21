FROM --platform=$BUILDPLATFORM node:16.16.0-alpine AS frontend

RUN mkdir /frontend
WORKDIR /frontend

COPY . .

RUN yarn global add @vue/cli
RUN yarn install
ENV HOST=0.0.0.0

ENTRYPOINT ["yarn", "run", "serve"]


