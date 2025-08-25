from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'
    # setup paypal ipn signal
    def ready(self):
        import payments.hooks
