from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile
from django.core.mail import send_mail
from root.settings import DEFAULT_FROM_EMAIL

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_delete, sender=CustomUser)
def delete_user_profile(sender, instance, **kwargs):
    """
    Delete the associated UserProfile when a CustomUser is deleted.
    """
    try:
        
        instance.profile.delete()
    except UserProfile.DoesNotExist:
        pass   

@receiver(pre_save, sender=CustomUser)
def send_role_update_email(sender, instance, **kwargs):
    """
    Signal to send email only when the user's role changes.
    """
    if instance.pk:  # Ensure the user exists (not being created)
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.role != instance.role:  # Role has changed
                subject = "Role Updated Notification"
                message = (
                    f"Hello {instance.email},\n\n"
                    f"Your role has been updated from {old_instance.role} to {instance.role}.\n\n"
                    "If you have any questions, please contact support.\n\n"
                    "Regards,\nE-commerce Team"
                )

                # Send email
                send_mail(
                    subject,
                    message,
                    DEFAULT_FROM_EMAIL,
                    [instance.email],
                    fail_silently=False,
                )
                print(f"Email sent: {old_instance.role} -> {instance.role}")  # Debugging log
        except sender.DoesNotExist:
            # Skip sending email if the old instance doesn't exist
            pass
