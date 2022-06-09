FROM node:lts-alpine
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY . .
RUN chmod +x entrypoint.sh

EXPOSE 8080
CMD ["sh", "entrypoint.sh"]