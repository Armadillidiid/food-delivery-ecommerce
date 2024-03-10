FROM nginx:1.25.4

# Set the working directory
WORKDIR /

# Add cron job to reload nginx every 24 hours
RUN echo "0 0 * * * root docker exec -it nginx nginx -s reload" > /etc/cron.d/nginx-job

# Download extra SSL configuration files
RUN curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > /options-ssl-nginx.conf && \
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > /ssl-dhparams.pem

# Set the default environment variable
ARG IS_SSL_ACQUIRED

# Create a directory for template files
RUN mkdir -p /etc/nginx/templates

# Copy template file based on SSL certificate acquisition
COPY ./default.conf.template /etc/nginx/templates/default.conf.template
COPY ./default.staging.conf.template /etc/nginx/templates/default.staging.conf.template

# Copy template file based on SSL certificate acquisition
RUN if [ "$IS_SSL_ACQUIRED" = "true" ]; then \
  rm /etc/nginx/templates/default.staging.conf.template; \
  else \
  rm /etc/nginx/templates/default.conf.template; \
  fi

# COPY proxy params
COPY ./proxy_params /etc/nginx/proxy_params
