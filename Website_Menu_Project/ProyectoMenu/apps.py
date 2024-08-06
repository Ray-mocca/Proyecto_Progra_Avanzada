from django.apps import AppConfig


class ProyectomenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ProyectoMenu'

    def ready(self):
        import ProyectoMenu.signals
