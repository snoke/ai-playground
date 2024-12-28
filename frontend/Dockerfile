FROM node:lts

RUN apt-get update && apt-get install -y npm

COPY . .
RUN npm install
EXPOSE 5173

CMD ["bash", "-c", "npm run dev --host"  ]

