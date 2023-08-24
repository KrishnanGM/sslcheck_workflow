import requests
import json
import ssl
import socket
import datetime
import pytz
from dateutil import parser

def get_ssl_expiry(domain):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
    conn.connect((domain, 443))
    cert = conn.getpeercert()
    return cert['notAfter']

def send_slack_notification(domain, days_left):
    slack_webhook = "https://hooks.slack.com/services/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" 
    message = f"SSL Expiry Alert\n* Domain : {domain}\n* Warning : The SSL certificate for {domain} will expire in {days_left} days."
    payload = { 
        "text": message
    }
    response = requests.post(slack_webhook, data=json.dumps(payload))
    return response.status_code == 200

def main():
    domain = "google.com"  # Specify the domain to check
    expiry_date_str = get_ssl_expiry(domain)
    expiry_date = parser.parse(expiry_date_str)
    current_date = datetime.datetime.now(pytz.utc)
    days_left = (expiry_date - current_date).days

    if days_left < 365:  # Customize the warning threshold as needed
        send_slack_notification(domain, days_left)

if __name__ == "__main__":
    main()

