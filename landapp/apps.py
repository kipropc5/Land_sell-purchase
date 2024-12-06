from django.apps import AppConfig


class LandappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landapp'
# apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'landapp'

    def ready(self):
        import landapp.signals  # Import the signals module
