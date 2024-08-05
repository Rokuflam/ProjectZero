# Use the base Nginx Alpine image
FROM nginx:alpine

# Set working directory
WORKDIR /etc/nginx

# Generate SSL certificates
RUN apk add --no-cache openssl \
    && openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
       -keyout certs/nginx.key -out certs/nginx.crt \
       -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=yourdomain.com"

# Copy the Nginx configuration file
COPY conf/default.conf /etc/nginx/conf.d/default.conf
