import faulthandler
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from modules.accounts.models import User, Customer
from modules.wallet.models import Wallet, Deposit


@receiver(post_save, sender=Customer)
def create_wallet(sender, instance, created, *args, **kwargs):
    if created:
        Wallet.objects.update_or_create(
            user=instance, account_name=f"{instance.user.username}'s")
