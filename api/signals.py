from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Billing

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Billing)
def send_billing_notify(sender, instance=None, created=False, **kwargs):
    if instance:
        usage_percent = (instance.no_of_request_consumed / instance.no_of_req_allowed) * 100
        
        if usage_percent == 100:
            # Send notification for 100% usage
            send_notification(instance.client, "You have used 100% of your allowed requests.")
        elif usage_percent == 90:
            # Send notification for 90% usage
            send_notification(instance.client, "You have used 90% of your allowed requests.")
        elif usage_percent == 50:
            # Send notification for 50% usage
            send_notification(instance.client, "You have used 50% of your allowed requests.")
            
def send_notification(client, message):
    # Logic to send notification
    print(f"Notification to {client.name}: {message}")