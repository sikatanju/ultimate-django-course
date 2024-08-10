from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpRequest
from django.http import HttpResponse
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializers, CollectionSerializer
from .models import Product, Collection


# Create your views here.
#* This bit of code is before adding 'POST' method:
# @api_view()
# def product_list(request):
#     query_set = Product.objects.select_related('collection').prefetch_related('promotions').all()
    
#     # product_list = get_list_or_404(query_set)
#     # product_list_seri = ProductSerializers(product_list, many=True)
    
#     #* We could have also pass the query_set directly to the:
#     product_list_seri = ProductSerializers(query_set, many=True, context={'request': request})
    
#     return Response(product_list_seri.data)

#* After adding 'POST' method:
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        query_set = Product.objects.select_related('collection').prefetch_related('promotions').all()
        product_list_seri = ProductSerializers(query_set, many=True, context={'request': request})
        
        return Response(product_list_seri.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializers(data=request.data)
        
        #* One way to do this :
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response("OK")
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #* Shorter way to do the same thing: 
        serializer.is_valid(raise_exception=True)

        #* Saving an object to the database
        serializer.save()
        # print(serializer.validated_data)
        return Response(serializer.data)


#* 'PUT' is used to update all properties & 'PATCH' is for update a subset of properties.
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    #* We could use these lines.
    # try:
    #     product_obj = Product.objects.get(pk=id)
    #     product_ser = ProductSerializers(product_obj)
    #     return Response(product_ser.data)
    
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    #* Or use a shortcut like this:
    product_obj = get_object_or_404(Product, pk=id)
    
    if request.method == "GET":
        product_seri = ProductSerializers(product_obj)
        return Response(product_seri.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'PUT':
        serializer = ProductSerializers(product_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':    
        if product_obj.orderitems.count() > 0:
            return Response({'errors': "Can't delete this product because it's associated with an order."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        product_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        # queryset = Collection.objects.all()
        # collection_seri = CollectionSerializer(queryset, many=True)
        # return Response(collection_seri.data)
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        new_collection = CollectionSerializer(data=request.data)
        new_collection.is_valid(raise_exception=True)
        new_collection.save()
        return Response(new_collection.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection_obj = get_object_or_404(Collection.objects.annotate(products_count=Count('products')).all(), pk=pk)
    
    if request.method == 'GET':
        collection_seri = CollectionSerializer(collection_obj)
        return Response(collection_seri.data)
    
    elif request.method == "PUT":
        collection_seri = CollectionSerializer(collection_obj, data=request.data)
        collection_seri.is_valid(raise_exception=True)
        collection_seri.save()
        return Response(collection_seri.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        if collection_obj.products.count() > 0:
            return Response({'Errors': "Can't delete this collection, because it's associated with other products"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        collection_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)