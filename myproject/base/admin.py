from django.contrib import admin
from .models import Products
# Register your models here.


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'pname', 'pcategory', 'price', 'trending', 'offer')
    list_filter = ('pcategory', 'trending', 'offer')
    search_fields = ('pname', 'pcategory')


'''
# create superuser

'''

