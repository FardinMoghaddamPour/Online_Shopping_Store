from django.core.mail import send_mail
from django.conf import settings


def send_verification_code(user_email, verification_code):
    subject = 'Authentication code: Tiny Instagram'
    message = f'Your authentication code is: {verification_code}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
