import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")

app = Celery("eshop")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "task1": {
        "task": "orders.tasks.place_order",
        # "schedule": crontab(minute="*/30", hour="8-19"),
        "schedule": crontab(),
    },
    # "task2": {
    #     "task": "orders.tasks.add_shipping_address",
    #     "schedule": crontab(minute="*/60", hour="12-14", day_of_week="1"),
    # },
    # "task2": {
    #     "task": "orders.tasks.create_users",
    #     "schedule": crontab(minute="*/60", hour="12-14", day_of_week="1,3"),
    # },
}
