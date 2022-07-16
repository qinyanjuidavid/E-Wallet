from modules.wallet.models import (Deposit, Transfer, Wallet,
                                   Withdrawal)
from rest_framework import serializers
from modules.accounts.serializers import CustomerProfileSerializer


class WalletSerializer(serializers.ModelSerializer):
    user = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ("id", "user", "balance", "account_name",
                  "account_number", 'bank_name', 'created_at',
                  'updated_at')
        read_only_fields = ('user',)


class DepositeSerializer(serializers.ModelSerializer):
    user = CustomerProfileSerializer(read_only=True)
    amount = serializers.FloatField(required=True)

    class Meta:
        model = Deposit
        fields = ("id", "user", "amount", "wallet", "created_at",
                  "updated_at")
        # read_only_fields = ('user',)


class WithdrawalSerializer(serializers.ModelSerializer):
    user = CustomerProfileSerializer(read_only=True)
    amount = serializers.FloatField(required=True)

    class Meta:
        model = Withdrawal
        fields = ("id", "user", "amount", "wallet", "created_at",
                  "updated_at")


class TransferSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)
    amount = serializers.FloatField(required=True)
    user = CustomerProfileSerializer(read_only=True)
    target_customer = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = Transfer
        fields = ("id", "user", "amount", "target_customer", "wallet", "created_at",
                  "updated_at")
