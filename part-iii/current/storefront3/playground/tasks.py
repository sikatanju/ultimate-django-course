from time import sleep
from celery import shared_task
from pprint import pprint

@shared_task
def notify_customer(message):
    pprint("Sending 10k emails..." + message)
    sleep(10)
    pprint('Emails were successfully sent!')