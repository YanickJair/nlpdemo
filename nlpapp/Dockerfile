# build stage
FROM node:lts-alpine as build-stage

WORKDIR /nlpapp

COPY package*.json ./

RUN yarn install

COPY . .

RUN yarn run build

# Production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /nlpapp/dist /usr/share/ngnix/html

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]