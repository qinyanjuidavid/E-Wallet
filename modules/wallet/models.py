from django.db import models
from django.utils.translation import gettext as _
from modules.accounts.models import (Administrator, Customer, TrackingModel,
                                     User)

# Wallet Management
# Deposit
# Withdrawal from wallet
# Transfer to different user


class Wallet(TrackingModel):
    user = models.OneToOneField(Customer, on_delete=models.SET_NULL, null=True)
    balance = models.FloatField(_("balance"), default=0)
    account_name = models.CharField(
        _("account name"), max_length=100, null=True)
    account_number = models.CharField(_("account number"),
                                      max_length=100, blank=True, null=True)
    bank_name = models.CharField(
        _("bank name"), max_length=100, blank=True, null=True)

    def __str__(self):
        return "{}'s wallet".format(self.user.user.username)

    class Meta:
        verbose_name_plural = _("wallets")


class Deposit(TrackingModel):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(_("amount"), default=0)
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} deposited {}".format(self.user.user.username, self.amount)

    class Meta:
        verbose_name_plural = _("Deposits")


class Withdrawal(TrackingModel):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(_("amount"), default=0)
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} withdrew {}".format(self.user.user.username, self.amount)

    class Meta:
        verbose_name_plural = _("Withdrawals")


class Transfer(TrackingModel):
    user = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name='sender')
    amount = models.FloatField(_("amount"), default=0)
    target_customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True
                               )

    def __str__(self):
        return "{} transfer to {}".format(self.sender.user.username, self.target_customer.username)

    class Meta:
        verbose_name_plural = "Transfer"


# class WalletTransaction(TrackingModel):
#     user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,relate)
#     amount = models.FloatField(_("amount"), default=0)
#     wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return "{}'s wallet transaction".format(self.user.username)

#     class Meta:
#         verbose_name_plural = "Wallet Transactions"
