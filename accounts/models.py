from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    reset_password_url = 'https://homebaba.ca/portal/password-reset/?token=' + \
        reset_password_token.key
    email_subject = 'Reset Your Password for Homebaba Portal'
    email_body = 'Hi,\n\nYou recently requested to reset your password for the Homebaba Portal. Please click on the link below to create a new password:\n\n{}\n\nIf you did not request a password reset, please ignore this email.\n\nKind Regards,\nThe Homebaba Team'.format(
        reset_password_url)

    send_mail(
        email_subject,
        email_body,
        'noreply@homebaba.ca',
        [reset_password_token.user.email],
        fail_silently=False,
    )


class Agent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    position = models.CharField(max_length=700, blank=True)
    agent_association = models.CharField(max_length=700, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
