from django.apps import AppConfig


class LockersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.lockers"
    verbose_name = "사물함 관리"
