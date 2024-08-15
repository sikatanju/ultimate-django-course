from django_filters.rest_framework import FilterSet

import django_filters

from .models import Product


class ProductFilter(FilterSet):
    #* This is from the documentation: 
    # any_price = django_filters.NumberFilter()
    # any_price__gt = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gt')
    # any_price__lt = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lt')


    class Meta:
        model = Product

        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt'],
        }