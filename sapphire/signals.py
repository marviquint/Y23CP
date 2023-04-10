from django.dispatch import Signal
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from sapphire.models import User
from django.utils.html import strip_tags

# Define a new signal called user_added
user_added = Signal()

@receiver(post_save, sender=User)
def send_user_login_details(sender, instance, created, **kwargs):
    if created:
        subject = 'Your login details for Sapphire'
        
        # Use the plaintext password in the email message
        password = instance.password
        message = f'Hello {instance.first_name},<br><br>Your Sapphire account has been created. Your login details are:<br><br>Email: <b>{instance.email}</b><br>Password: <b>{instance.password}</b><br><br><br><p style="color:red;"><b>***NOTE***</b></p><br>• Please keep these details safe and do not share them with anyone.<br>• The password being sent to you is hashed for security purposes, just <b>COPY and PASTE</b> the password when logging int.<br>•The password provided is just a temporary and one-time use password, please go to your profile to change your password immediately.<br><br>Best Regards,<br><b>Sapphire Admin</b>'
        recipient_list = [instance.email]
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, strip_tags(message), from_email, recipient_list, html_message=message, fail_silently=False)
        
        # Set the password back to its hashed format (not recommended)
        hashed_password = make_password(password)
        instance.password = hashed_password
        instance.save(update_fields=['password'])
        
        # If the user is logging in for the first time, set the "show_modal" attribute to True
        if instance.last_login is None:
            instance.show_modal = True
            instance.save(update_fields=['show_modal'])
            
