from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.signals import worker_ready
from django.conf import settings
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Tehran')

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

# Todo : Check Inspection CTRL ALT S


@app.task(bind=True)
def debug_task(self):
    # noinspection PyCompatibility
    print(f'Request: {self.request!r}')


@worker_ready.connect
def at_start(sender, **kwargs):
    from account.tasks import delete_inactive_users
    delete_inactive_users.apply_async()
