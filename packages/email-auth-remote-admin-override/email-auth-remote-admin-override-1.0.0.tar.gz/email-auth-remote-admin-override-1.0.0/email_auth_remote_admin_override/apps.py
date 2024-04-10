from django.apps import AppConfig


class AdminOverrideConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "email_auth_remote.admin_override"
