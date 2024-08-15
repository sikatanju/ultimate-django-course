from decimal import Decimal

import datetime

from rest_framework import serializers

from django.db.models import Count

from .models import Product, Collection, Review


# class CollectionSerializers(serializers.Serializer):
#     collection_id = serializers.IntegerField(source='id')
#     collection_name = serializers.CharField(max_length=255, source='title')

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    

    #* This is done by Mosh:
    products_count = serializers.IntegerField(read_only=True)
    
    #* This is my implementation
    # products_count = serializers.SerializerMethodField(method_name='products_count_method')
    
    # def products_count_method(self, collection: Collection):
    #     count = Product.objects.filter(collection_id=collection.id).aggregate(Count('id'))
    #     return count['id__count']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        #* WE could add custom fields as well: 
        fields = ['id', 'title', 'description','slug', 'unit_price', 'price_with_tax', 'collection']
        
        #* Just trying out the hyperlink for collection option: 
        # fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']
        
        #* To get all the fields in the product class: 
        # fields = '__all__'

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1) 
    
    # * This is from ModelSerializer, we're overriding this method to add inventory field to 10, then saving the product]
    #* When we call 'serializer.save()' from the views, this method is called automatically.
    def create(self, validated_data):
        product = Product(**validated_data)
        #* Since, we're not passing inventory fields through the api, we're adding it here under the hood.
        product.inventory = 10
        product.save()
        return product
    
    #* Similary to 'create()' method, there is 'update()' method:
    def update(self, instance, validated_data):
        instance.inventory = 100
        instance.save()
        return super().update(instance, validated_data)
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']
        

    # date = serializers.DateField(read_only=True)

    def create(self, validated_data):
        # product_id = self.context['product_id']
        return Review.objects.create(product_id=self.context['product_id'], **validated_data)

#* This bit of code is repititive, better way to implement this is to use 'ModelSerializer'

# class ProductSerializers(serializers.Serializer):    
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=4, decimal_places=2, source='unit_price')
#     price_incl_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
#     #* This is one way to get related fields
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset=Collection.objects.all()
#     # )

#     #* Another way to add the related fields:
#     # collection = serializers.StringRelatedField(
#     #     # queryset=Collection.objects.all()
#     # )

#     #* To nested a collection object with each product:
#     # collection = CollectionSerializers()

#     #* We could also use a hyper link, which would take us to another page containing collection detail:
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name='collection-detail'
#     )

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.1)