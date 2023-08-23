#!/bin/bash

check_ssl_expiry() {
  domain="$1"
  expiry_date=$(openssl s_client -servername "$domain" -connect "$domain":443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
  remaining_days=$(( ($(date -d "$expiry_date" +%s) - $(date +%s)) / 86400 ))

  echo "Domain: $domain, Expiry Date: $expiry_date, Remaining Days: $remaining_days"

  if [ "$remaining_days" -lt 210 ]; then
    send_slack_alert "$domain" "$remaining_days"
  fi
}

send_slack_alert() {
  domain="$1"
  remaining_days="$2"
  message="SSL Expiry Alert\n   * Domain : $domain\n   * Warning : The SSL certificate for $domain will expire in $remaining_days days."

  curl -X POST -H 'Content-type: application/json' --data "{
    \"text\": \"$message\"
  }" "$SLACK_WEBHOOK_"
}

while IFS= read -r domain || [[ -n "$domain" ]]; do
  if [ -n "$domain" ]; then
    echo "Processing domain: $domain"
    check_ssl_expiry "$domain"
  fi
done < "$(dirname "$0")/domains.txt"

