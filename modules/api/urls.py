from modules.accounts.views import CustomerRegistrationViewSet, LoginViewSet
from modules.wallet.views import DepositeAPIView, TransferAPIView, WalletAPIView, WithdrawalAPIView
from rest_framework.routers import SimpleRouter
from django.views.generic import TemplateView
from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)


app_name = "api"
routes = SimpleRouter()

routes.register("login", LoginViewSet,
                basename="login")
routes.register("register", CustomerRegistrationViewSet,
                basename="register")
routes.register("wallet", WalletAPIView, basename="wallet")
routes.register("deposite", DepositeAPIView, basename="deposite")
routes.register("withdraw", WithdrawalAPIView, basename="withdraw")
routes.register("transfer", TransferAPIView, basename="transfer")

urlpatterns = [
    *routes.urls
]
