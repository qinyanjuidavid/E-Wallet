from django.contrib import admin
from modules.wallet.models import Deposit, Transfer, Wallet, Withdrawal

admin.site.register(Deposit)
admin.site.register(Transfer)
admin.site.register(Wallet)
admin.site.register(Withdrawal)
