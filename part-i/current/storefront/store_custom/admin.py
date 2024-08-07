from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


# Register your models here.
class TaggedInline(GenericTabularInline):
    model = TaggedItem
    extra = 1
    autocomplete_fields = ['tag']

# @admin.register(Product)
class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)