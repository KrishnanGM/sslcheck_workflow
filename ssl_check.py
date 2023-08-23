import requests
import json
import ssl
import socket
import datetime
import pytz
from dateutil import parser
import os
import sys

def get_ssl_expiry(domain):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
    conn.connect((domain, 443))
    cert = conn.getpeercert()
    return cert['notAfter']

def send_slack_notification(domain, days_left, slack_webhook):
    message = f"SSL Expiry Alert\n* Domain : {domain}\n* Warning : The SSL certificate for {domain} will expire in {days_left} days."
    payload = {
        "text": message
    }
    response = requests.post(slack_webhook, data=json.dumps(payload))
    return response.status_code == 200

def main():
    with open("domains.txt") as file:
        domains = [line.strip() for line in file.readlines()]

        slack_webhook = sys.argv[1]


    for domain in domains:
        expiry_date_str = get_ssl_expiry(domain)
        expiry_date = parser.parse(expiry_date_str)
        current_date = datetime.datetime.now(pytz.utc)
        days_left = (expiry_date - current_date).days

        if days_left < 365:  # Customize the warning threshold as needed
            send_slack_notification(domain, days_left, slack_webhook)

if __name__ == "__main__":
    main()
