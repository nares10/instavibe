from django.apps import AppConfig


class nexusappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nexusapp'

    def ready(self):
        import nexusapp.signals.profile  # Ensure signals are imported and registered
        import nexusapp.signals.notifications