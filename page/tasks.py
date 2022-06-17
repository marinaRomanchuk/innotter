from django.core.mail import send_mail
import os

from innotter.celery import app
from .models import Page


@app.task
def send_message(
    subject="New post", message="Visit Innotter to see new post.", receivers=()
):
    send_mail(
        subject,
        message,
        os.getenv("EMAIL_HOST_USER"),
        receivers,
        fail_silently=False,
    )


@app.task
def unblock_page(page_id: int):
    Page.objects.filter(pk=page_id).update(unblock_date=None)
