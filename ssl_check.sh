#!/bin/bash

check_ssl_expiry() {
  domain="$1"
  expiry_date=$(openssl s_client -servername "$domain" -connect "$domain":443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
  remaining_days=$(( ($(date -d "$expiry_date" +%s) - $(date +%s)) / 86400 ))

  if [ "$remaining_days" -lt 200 ]; then
    send_slack_alert "$domain" "$remaining_days"
  fi
}

send_slack_alert() {
  domain="$1"
  remaining_days="$2"
  message="SSL Expiry Alert\n   * Domain : $domain\n   * Warning : The SSL certificate for $domain will expire in $remaining_days days."

  curl -X POST -H 'Content-type: application/json' --data "{
    \"text\": \"$message\"
  }" "$SLACK_WEBHOOK_URL"
}

while IFS= read -r domain || [[ -n "$domain" ]]; do
  echo "Processing domain: $domain"
  check_ssl_expiry "$domain"
done < "domains.txt"

