from celery import shared_task
import requests
from time import sleep


def send_email(email, subject, content):
    sender = 'app-noreply@email.suhaibwebb.com'
    url = "https://api.sendinblue.com/v3/smtp/email"
    headers = {}
    headers["accept"] = "application/json"
    headers["api-key"] = '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'
    headers["content-type"] = "application/json"

    data = '{"sender": {"name": "Swiss Web", "email":"' + sender + '"},' \
                                                                   '"to":[{"email":"' +email+ '"}], "subject":"' + \
           subject+ '",' \
                     '"htmlContent":"' + content + '"}'

    res = requests.post(url, headers=headers, data=data)


@shared_task()
def delivery_email(email, subject, content):
    sleep(6)
    send_email(email, subject, content)
    return 'Email-Sent'