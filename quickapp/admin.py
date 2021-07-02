from django.contrib import admin
from .models import customer, orders, salesperson


# Register your models here.
admin.site.register(customer)
admin.site.register(orders)
admin.site.register(salesperson)