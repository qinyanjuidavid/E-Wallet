from django.contrib import admin
from modules.accounts.models import (User, Customer, Administrator)

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Administrator)
