# Stage 1: build the Vite bundle
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# VITE_API_URL / VITE_CUSTOMER_TOKEN can be injected at build time.
ARG VITE_API_URL=http://localhost:8080
ARG VITE_CUSTOMER_TOKEN=
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_CUSTOMER_TOKEN=$VITE_CUSTOMER_TOKEN
RUN npm run build

# Stage 2: serve static files with nginx
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
