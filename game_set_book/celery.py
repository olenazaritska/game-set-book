import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game_set_book.settings")

app = Celery("game_set_book")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
