from django.apps import AppConfig


class SapphireConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sapphire'

    def ready(self):
        import sapphire.signals

    # def ready(self):
    #     # Import the necessary signal and model inside the ready method
    #     from django.db.models.signals import post_save
    #     from django.dispatch import receiver
    #     from sapphire.signals import send_user_notification
    #     from sapphire.models import User

    #     # Connect the post_save signal of the User model to the send_user_notification function
    #     post_save.connect(send_user_notification, sender=User)