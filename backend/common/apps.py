from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'

    def ready(self):
       
        import products.signals
        
        from django.db.utils import OperationalError
        from common.models import Role   

        ROLE_CHOICES = (
        ('super_user', 'SuperUser'),
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('end_user', 'EndUser'),
        )

        try:
            for role_name, _ in ROLE_CHOICES:
                if not Role.objects.filter(name=role_name).exists():
                    Role.objects.create(name=role_name)
        except OperationalError:
            pass


