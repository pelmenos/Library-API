from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'

    # def ready(self):
    #     import os
    #     if os.environ.get('RUN_MAIN') or not os.environ.get('DJANGO_AUTO_RELOAD'):
    #         from .scheduler import start_scheduler
    #         start_scheduler()
