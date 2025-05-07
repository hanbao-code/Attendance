from django.apps import AppConfig
import django_cron

class AttenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Atten'

    def ready(self):
        django_cron.autodiscover()
