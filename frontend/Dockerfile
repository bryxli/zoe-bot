FROM node:latest as build
WORKDIR /app
COPY . .
RUN yarn && yarn build

FROM nginx:alpine
RUN mkdir -p /usr/share/nginx/html
RUN mkdir -p /etc/nginx/conf.d
COPY --from=build /app/build /usr/share/nginx/html
COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]