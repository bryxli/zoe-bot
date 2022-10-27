FROM node:latest
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json .
COPY yarn.lock .
RUN yarn
EXPOSE 3000
COPY . .
CMD ["yarn", "start"]