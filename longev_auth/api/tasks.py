import smtplib

from celery import shared_task
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response


@shared_task
def send_email(
    subject: str,
    body: str,
    from_email: str,
    to: list[str],
    reply_to: list[str],
    content_subtype: str = "html",
):
    """Function to send email"""
    mail = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
        reply_to=reply_to,
    )
    mail.content_subtype = content_subtype
    try:
        mail.send(fail_silently=False)
    except smtplib.SMTPSenderRefused as e:
        return Response({"data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return True
