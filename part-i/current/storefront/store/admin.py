from typing import Any

from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode

from .models import *


#* Class for CustomeQueryFilter
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [('<10', 'Low')]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


#* For reference, go to `Django ModelAdmin` docs
# Register your models here.
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        # return collection.products_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


# class TagInline(GenericTabularInline):
#     model = TaggedItem
#     extra = 0
#     autocomplete_fields = ['tag']

# * Either we could do this : 
# class ProductAdmin(admin.ModelAdmin):
#     list_display=['title', 'unit_price']

# admin.site.register(Product, ProductAdmin)


#* Or do the same thing this way:
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']  #* Now this would be editable in the admin page
    list_per_page = 100

    search_fields = ['title']

    #* It works just like select_releated we learned in ORM, it loads releadted objects
    list_select_related = ['collection']

    list_filter = ['collection', 'last_update', InventoryFilter]

    prepopulated_fields = {
        'slug': ['title']
    }

    autocomplete_fields = ['collection']

    # inlines = [TagInline]

    #* `collection_title` isn't defined so, we have to create a method with that name:
    #* Also, for sorting: 
    @admin.display(ordering='collection')
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'

        return 'Ok'

    @admin.action(description='clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=1)
        self.message_user(request, f'{updated_count} products were successfully updated', messages.SUCCESS)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    fields = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 100
    ordering = ['first_name', 'last_name']

    search_fields = ['first_name', 'last_name']


class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = OrderItem
    extra = 0
    max_num = 10


#* Exercise
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['payment_status', 'placed_at', 'customer_full_name']
    list_per_page = 100
    list_select_related = ['customer']
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']

    @admin.display(ordering='customer')
    def customer_full_name(self, order):
        return order.customer.__str__()
