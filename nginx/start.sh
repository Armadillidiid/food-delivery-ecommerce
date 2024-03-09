#!/bin/bash

domains=($SERVER_NAME)
rsa_key_size=4096
data_path="../data/certbot" # Path should correspond to the volume mounted in docker-compose.yml
email=$CERTBOT_EMAIL
staging=1 # Set to 1 to avoid hitting request limits

if [ -d "$data_path" ]; then
	read -p "Existing data found for $domains. Continue and replace existing certificate? (y/N) " decision
	if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
		exit
	fi
fi

echo "### Requesting Let's Encrypt certificate for $domains ..."
#Join $domains to -d args
domain_args=""
for domain in "${domains[@]}"; do
	domain_args="$domain_args -d $domain"
done

# Select appropriate email arg
case "$email" in
"") email_arg="--register-unsafely-without-email" ;;
*) email_arg="--email $email" ;;
esac

# Enable staging mode if needed
if [ $staging != "0" ]; then staging_arg="--staging"; fi

docker compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot
