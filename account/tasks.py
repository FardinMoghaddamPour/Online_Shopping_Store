from celery import shared_task
from utils.send_email_to_user import send_verification_code


# noinspection PyUnusedLocal
@shared_task(bind=True)
def send_verification_code_to_user(self, user_email, verification_code):
    print(f"Task started: Sending email to {user_email} with code {verification_code}")
    send_verification_code(user_email, verification_code)
    print(f"Email sent to ==> {user_email}")
    return "Done"
