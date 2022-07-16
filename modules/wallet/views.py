from django.shortcuts import get_object_or_404, render
from modules.accounts.models import Customer
from modules.accounts.permissions import IsAdministrator, IsCustomer
from modules.wallet.models import Deposit, Transfer, Wallet, Withdrawal
from modules.wallet.serializers import DepositeSerializer, TransferSerializer, WalletSerializer, WithdrawalSerializer
from rest_framework import generics, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q


class WalletAPIView(ModelViewSet):
    serializer_class = WalletSerializer
    permission_classes = [IsCustomer]
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        user = self.request.user
        customerQuery = Customer.objects.get(user=user)

        walletQs = Wallet.objects.filter(
            Q(user=customerQuery)
        )
        return walletQs

    def retrieve(self, request, pk, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(
            queryset, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        queryset.bank_name = serializer.validated_data['bank_name']
        queryset.account_name = serializer.validated_data['account_name']
        queryset.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepositeAPIView(ModelViewSet):
    serializer_class = DepositeSerializer
    permission_classes = [IsCustomer]
    http_method_names = ['post', "get", ]

    def get_queryset(self):
        user = self.request.user
        customerQuery = Customer.objects.get(user=user)
        depositQs = Deposit.objects.filter(Q(user=customerQuery))
        return depositQs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        customerQuery = Customer.objects.get(user=user)
        walletQs = Wallet.objects.get(user=customerQuery)
        serializer.save(user=customerQuery, wallet=walletQs)
        walletQs.balance += serializer.data["amount"]
        walletQs.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WithdrawalAPIView(ModelViewSet):
    serializer_class = WithdrawalSerializer
    permission_classes = [IsCustomer]
    http_method_names = ['post', "get", ]

    def get_queryset(self):
        user = self.request.user
        customerQuery = Customer.objects.get(user=user)
        withdrawal = Withdrawal.objects.filter(Q(user=customerQuery))
        return withdrawal

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        customerQuery = Customer.objects.get(user=user)
        walletQs = Wallet.objects.get(user=customerQuery)
        if serializer.validated_data["amount"] > walletQs.balance:
            return Response({"message": "Insufficient funds"},
                            status=status.HTTP_200_OK)
        else:
            serializer.save(user=customerQuery, wallet=walletQs)
            walletQs.balance -= serializer.data["amount"]
            walletQs.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransferAPIView(ModelViewSet):
    serializer_class = TransferSerializer
    permission_classes = [IsCustomer]
    http_method_names = ['post', 'get', ]

    def get_queryset(self):
        user = self.request.user
        customerQuery = Customer.objects.get(user=user)
        transferQs = Transfer.objects.filter(Q(user=customerQuery))
        return transferQs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        customerQuery = Customer.objects.get(user=user)
        walletQs = Wallet.objects.get(user=customerQuery)
        if serializer.validated_data["amount"] > walletQs.balance:
            return Response({"message": "Insufficient funds"},
                            status=status.HTTP_200_OK)
        else:
            serializer.save(user=customerQuery, wallet=walletQs)
            walletQs.balance -= serializer.data["amount"]
            walletQs.save()
        # target_customer_Qs = Customer.objects.get(
        #     id=serializer.data["target_customer"])
        # target_wallet_Qs = Wallet.objects.get(user=target_customer_Qs)
        # target_wallet_Qs.balance += serializer.data["amount"]
        # target_wallet_Qs.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
