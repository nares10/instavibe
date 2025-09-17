from django.apps import AppConfig


class InstavibeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instavibeapp'

    def ready(self):
        import instavibeapp.signals.profile  # Ensure signals are imported and registered
        import instavibeapp.signals.notifications