from django.db.models.signals import (
    post_save,
    post_migrate)
from django.dispatch import receiver

from modules.accounts.models import (User, Administrator, Customer)


@receiver(post_save, sender=User)
def create_users(sender, instance, created, *args, **kwargs):
    if created:
        if (instance.role == "Administrator" or
                instance.is_admin or instance.is_staff):
            Administrator.objects.update_or_create(user=instance)
        elif (instance.role == "Customer"):
            Customer.objects.update_or_create(user=instance)
