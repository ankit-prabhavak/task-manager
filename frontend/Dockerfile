# --- Build stage ---
FROM node:20-alpine AS build

WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .

# Vite reads VITE_ variables at BUILD time and bakes them into the
# compiled JS, so we accept it as a build argument.
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# --- Serve stage ---
# nginx is a lightweight web server, perfect for serving the static
# files Vite produces.
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
