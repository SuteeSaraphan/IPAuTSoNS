FROM --platform=$BUILDPLATFORM node:16.16.0-alpine AS frontend

RUN mkdir /ipuatsons
WORKDIR /ipuatsons

COPY . .

RUN yarn global add @vue/cli
RUN yarn install
ENV HOST=0.0.0.0

CMD ["yarn", "run", "serve"]


