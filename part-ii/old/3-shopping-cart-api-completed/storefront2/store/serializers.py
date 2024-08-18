from decimal import Decimal
from uuid import uuid4

from rest_framework import serializers

from django.db.models import Count

from .models import Product, Collection, Review, Cart, CartItem


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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']
    

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id',  'product', 'quantity', 'total_price']

    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    
    def get_total_price(self, cart: Cart):
        return sum([(item.product.unit_price*item.quantity) for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class CreateCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There isn't any product available by the given product_id")
        
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        print(cart_id)
        product_id = self.validate_product_id(self.validated_data['product_id'])
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    # product = SimpleProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        # fields = ['id', 'product', 'quantity', 'total_price']
        fields = ['quantity']

    # total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    # def calculate_total_price(self, cart_item: CartItem):
    #     return cart_item.quantity * cart_item.product.unit_price

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