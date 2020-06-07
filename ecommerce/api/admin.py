from django.contrib import admin

from .models import Seller, Product, Purchase

admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Purchase)
