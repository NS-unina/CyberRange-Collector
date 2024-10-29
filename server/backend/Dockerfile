FROM node:14

WORKDIR /usr/src/app

COPY package.json ./

RUN npm install

COPY . .

EXPOSE 9000

# CMD ["npm", "start"]
CMD ["npx", "nodemon", "server.js"]
