import requests
import os

def send_email(to_send, subject, html):
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {"email": "business.simplemeet@gmail.com"},
        "to": [{"email": to_send}],
        "subject": subject,
        "htmlContent": html
    }

    headers = {
        "accept": "application/json",
        "api-key": os.getenv("EMAIL_API_KEY"),
        "content-type": "application/json"
    }
    print(headers["api-key"])
    #response = requests.post(url, json=payload, headers=headers)
    #print(response.status_code, response.text)
    print("sent")
