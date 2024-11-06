FROM nginx:latest

RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/nginx.conf

ARG NGINX_PORT
EXPOSE ${NGINX_PORT}

CMD ["nginx", "-g", "daemon off;"]