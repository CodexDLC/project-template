# Base Image: Nginx Alpine (Lightweight)
FROM nginx:alpine

# Copy Main Configuration
# Assumes build context is the repository root
COPY nginx/nginx-main.conf /etc/nginx/nginx.conf

# Copy Site Configuration (Server Block)
COPY nginx/site.conf /etc/nginx/conf.d/default.conf

# Copy Frontend Static Files
COPY frontend /usr/share/nginx/html

# Create Certbot directory (prevents startup errors if volume is missing)
RUN mkdir -p /var/www/certbot

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
