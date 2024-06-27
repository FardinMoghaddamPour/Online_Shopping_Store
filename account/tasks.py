from time import sleep
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from utils.send_email_to_user import send_verification_code
from .models import CustomUser
import pytz


# noinspection PyUnusedLocal
@shared_task(bind=True)
def send_verification_code_to_user(self, user_email, verification_code):
    print(f"Task started: Sending email to {user_email} with code {verification_code}")
    send_verification_code(user_email, verification_code)
    print(f"Email sent to ==> {user_email}")
    return "Done"


# noinspection PyUnusedLocal
@shared_task(bind=True)
def delete_inactive_users(self):

    current_time_utc = timezone.now()
    local_timezone = pytz.timezone('Asia/Tehran')
    current_time_tehran = current_time_utc.astimezone(local_timezone)

    three_days_ago = current_time_tehran - timedelta(days=3)

    inactive_users = CustomUser.objects.filter(is_active=False, create_at__lt=three_days_ago)
    if inactive_users:
        print("Deleting inactive users")
        sleep(10)
    else:
        print("None")

    deleted_count = inactive_users.delete()
    return f"Deleted {deleted_count} inactive users."
