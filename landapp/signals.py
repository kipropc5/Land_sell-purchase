# signals.py
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Land App!'
        message = f'Hi {instance.username}, thank you for registering at Land App.'
        sender_mail = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        try:
            send_mail(subject, message, sender_mail, recipient_list)
            logger.info(f'Welcome email sent to {instance.email}')
        except Exception as e:
            logger.error(f'Failed to send welcome email: {e}')
