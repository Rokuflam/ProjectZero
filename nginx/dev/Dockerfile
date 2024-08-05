# Use the base Nginx Alpine image
FROM nginx:alpine

# Set working directory
WORKDIR /etc/nginx

# Create a directory for certificates
RUN mkdir -p /etc/nginx/certs

# Generate SSL certificates
RUN apk add --no-cache openssl \
    && openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
       -keyout /etc/nginx/certs/nginx.key -out /etc/nginx/certs/nginx.crt \
       -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=yourdomain.com"

# Copy the Nginx configuration file
COPY conf/default.conf /etc/nginx/conf.d/default.conf