from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F, Min, Max, Avg, Sum, Count, Value, Func, ExpressionWrapper
from django.db.models.functions import Concat
from django.db import transaction, connection


from store.models import *
from tags.models import TaggedItem


def say_hello(request):
    # try:
    #     product = Product.objects.get(id=1)
    # except ObjectDoesNotExist:
    #     print("Object does not exists")

    #None
    # product = Product.objects.filter(pk=1).first()

    #* Check if an object exists or not
    # exists = Product.objects.filter(id=1).exists()

    return render(request, 'hello.html', {'name': 'Sika'})

# * This is for performing simple query.
# def practice(request):
#     # query_set = Product.objects.filter(title__contains='coffee') #* Case-sensitive
#     query_set = Product.objects.filter(title__icontains='coffee') #* Not case-sensitive
#     # query_set = Product.objects.filter(title__icontains='coffee')
#     # query_set = Product.objects.filter(unit_price__gte=10)
#     # query_set = Product.objects.filter(unit_price__range=(10, 11)) #* In range, from 10 -> 11 (inclusive)
#     # query_set = Product.objects.filter(description__isnull=True) #* Checking a null field

#     return render(request, 'practice.html', {'products': list(query_set)})

# * This is for complex query building:
# def practice(request):
#     #* Using `and` operator is easy, just pass two condition separated by comma.
#     # query_set = Product.objects.filter(unit_price__lt=10, inventory__gt=10)
    
#     #* Another way of doing the same operation:
#     # query_set = Product.objects.filter(unit_price__lt=10).filter(inventory__gt=10)


#     # *** Now, let's try out some compound query using `or` operator:
#     # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=10))

#     #* We could also use `~` to perform not on a condition
#     # Here, the query is saying, get all the products where inventory is less than 10 or unit_price is not less than 10
#     # query_set = Product.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__lt=100))

#     # * Using `F` object to compare two fields
#     # query_set = Product.objects.filter(inventory=F('collection__id'))
    

#     return render(request, 'practice.html', {'products': list(query_set)})


# ** Sorting data: 
# def practice(request):
#     # query_set = Product.objects.order_by('title') # * Return in asc order
#     #* Returns in desc order
#     # query_set = Product.objects.order_by('-title')
#     #* Another way to achieve the same result:
#     # query_set = Product.objects.order_by('title').reverse()

#     #* Of course, we could first filter the data, then sort it by any field
#     # * We could also pass multiple order by as we learned in MySql course.
#     # query_set = Product.objects.filter(unit_price__lt=10).order_by('title', 'unit_price')

#     # return render(request, 'practice.html', {'products': list(query_set)})


#     #* Now to get only one product, let's the first one after sorting:
#     # product = Product.objects.order_by('title').first()
#     # * Above and below query is same
#     # product = Product.objects.order_by('title')[0]
#     # return render(request, 'practice.html', {'single_product': product})
    
#     #* Or another way of doing this: 
#     # product = Product.objects.earliest('title')
#     #* We could also do `latest`
#     product = Product.objects.latest('title')
#     return render(request, 'practice.html', {'single_product': product})


# ** Limiting data:
# def practice(request):
#     # query_set = Product.objects.filter(unit_price__lt=10)[:5] #* We're going to get the first 5 product
#     # query_set = Product.objects.filter(unit_price__lt=10)[5:10] #* Skiping first 5, then getting second 5
    
#     query_set = Product.objects.filter(unit_price__lt=10).order_by('title').reverse()[:5]

#     return render(request, 'practice.html', {'products': list(query_set)})


# ** Selecting fields to query: (selecting specific field(s) to perform query) 
# def practice(request):
#     # query_set = Product.objects.values('title', 'id') # * This should return only 'id', and 'unit_price' column
#     # query_set = Product.objects.values('unit_price', 'id') # * This should return only 'id', and 'unit_price' column
    
#     #* Performing related fields query:
#     # query_set = Product.objects.values("id", 'title', 'collection__title')
    
#     # * Now, values_list() returns a list of tuple, instead of dictionaries
#     # query_set = Product.objects.values_list("id", 'unit_price', 'collection__title')
    
#     #* Exercise:
#     # query_set = Product.objects.values('id', 'title', 'orderitem__product_id').distinct().order_by('title')
#     # * Another way to do the same query:
    # query_set = Product.objects.values('title').filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    
#     return render(request, 'practice.html', {'products' : list(query_set)})

# ** Deferring Fields: (use it with caution, otherwise it's gonna pass a lot of queries.)
# def practice(request):
#     # query_set = Product.objects.only('id', 'title')
    
#     # * Defer() is the opposite of only()
#     query_set = Product.objects.defer('id', 'title')
#     return render(request, 'practice.html', {'products' : list(query_set)})


# ** Selecting Related Fields: 
# def practice(request):
    # * It basically join two table
    # query_set = Product.objects.select_related('collection').all()

    #* For many-to-many relation, we use:
    # query_set = Product.objects.prefetch_related('promotions').defer('description')
    # query_set = Product.objects.prefetch_related('promotions').select_related('collection').order_by('title')

    # ** Exercise:
    # query_set = Order.objects.order_by('placed_at').reverse()[:5]

    # query_set = Order.objects.select_related('customer').order_by('placed_at').reverse()[:5]
    # query_set = OrderItem.objects.select_related('order').filter(order_id__in=Order.objects.values('id').distinct().order_by('-placed_at')[:5]).order_by('id')
    
    # * Exercise Solution
    # query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('placed_at').reverse()[:5]

    # return render(request, 'practice.html', {'orders' : list(query_set)})

# ** Aggregate Function:
# def practice(request):
#     # Basic
#     single_result = Product.objects.aggregate(Count('id'))
    
#     # We can specify it's name, also perform multiple operation
#     # single_result = Product.objects.aggregate(count=Count('id'),  min_price=Min('unit_price'))

#     #* Also we could filter data beforehand: 
#     single_result = Product.objects.filter(collection_id__gt=5).aggregate(count=Count('id'), min_price=Min('unit_price'))
#     return render(request, 'practice.html', { 'single_result' : single_result })


# ** Annotate Object: (to my understanding 'annotating object is just adding a new column with specified value')
# def practice(request):
#     #* Here, we're adding a new column to every customer object 'is_new' & set it's value to 'True'
#     # query_set = Customer.objects.annotate(is_new=Value(True)) #* The changes are not saved in the database though.

#     #* We could reference another field of the existing database to the new database, also preform computation
#     query_set = Customer.objects.annotate(new_id= F('id') +1)

#     return render(request, 'practice.html', {'name': 'Sika', 'products': list(query_set)})

#** Calling Database Function:
# def practice(request):
#     #* Calling `CONCAT` function of the database, and annotating that as `full_name`
#     # query_set = Customer.objects.annotate(full_name=Func(F('first_name'),Value(' - '),F('last_name'), function='CONCAT'))
    
#     #* There is a shortcut for the above query:
#     query_set = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))

#     # *** But for calling unique function of a specific database, we have to use the `Func` object
    
#     return render(request, 'practice.html', {'name': 'Sika', 'results': list(query_set)})

# ** Grouping Data:
# def practice(request):
#     query_set = Customer.objects.annotate(order_count=Count('order'))
    
#     # * This below sql got executed:
    
#     """
#       SELECT `store_customer`.`id`,
#        `store_customer`.`first_name`,
#        `store_customer`.`last_name`,
#        `store_customer`.`email`,
#        `store_customer`.`phone`,
#        `store_customer`.`birth_date`,
#        `store_customer`.`membership`,
#        COUNT(`store_order`.`id`) AS `order_count`
#         FROM `store_customer`
#         LEFT OUTER JOIN `store_order`
#             ON (`store_customer`.`id` = `store_order`.`customer_id`)
#         GROUP BY `store_customer`.`id`
#         ORDER BY NULL
#     """
#     return render(request, 'practice.html', {'results': list(query_set)})


# ** Expression Wrappers, used when we have to perform an operation we couldn't do in expression (eg. Value(), F(), Func())
# def practice(request):
#     discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=models.DecimalField())
#     query_set = Product.objects.annotate(discounted_price=discounted_price)

#     """ Executed SQL:
#     SELECT `store_product`.`id`,
#         `store_product`.`title`,
#         `store_product`.`slug`,
#         `store_product`.`description`,
#         `store_product`.`unit_price`,
#         `store_product`.`inventory`,
#         `store_product`.`last_update`,
#         `store_product`.`collection_id`,
#         (`store_product`.`unit_price` * 0.8e0) AS `discounted_price`
#     FROM `store_product`
#     """
#     return render(request, 'practice.html', {'results': list(query_set)})


# ** Querying Generic Relationship:

# def practice(request):
#     #* Defining Customer Manger for TaggedItem with below functionality.
#     # content_type = ContentType.objects.get_for_model(Product)
    
#     # queryset = TaggedItem.objects \
#     #     .select_related('tag') \
#     #     .filter(
#     #         content_type=content_type, 
#     #         object_id=1
#     #     )

#     queryset = TaggedItem.objects.get_tags_for(Product, 1)    
#     return render(request, 'practice.html', {'result': list(queryset)})



# *** CRUD operation using Django:

def django_crud(request):
    #** Creating an object:
    # Collection.objects.create(title='Video Game', featured_product_id=1) #* This is one way
    # new_collection = Collection()
    # new_collection.title = 'Video Game'
    # # new_collection.featured_product_id = 1 
    # # #* Either above line or below line
    # new_collection.featured_product = Product(pk=1)
    # new_collection.save()

    # ** Updating an object:
    
    #* To update an object, first read that object from the database, then update only the required field and save it back
    # new_collection = Collection.objects.get(pk=11)
    # new_collection.title = 'Video Game'
    # # new_collection.featured_product_id = 2
    # # #* Either above line or below line
    # new_collection.featured_product = Product(pk=2) #* 'PK' refers to `Primary Key`
    # new_collection.save()

    # ** Now, if reading from the database first causing your app to underperform, use below method:
    # Collection.objects.filter(pk=11).update( featured_product=None, title="Video G")

    #** Deleting an object:

    #* Simple approach to delete an object
    # delete_object = Collection.objects.get(pk=1)
    # delete_object.delete()

    #* To delele multiple objects:
    Collection.objects.filter(pk__gt=10).delete()

    return render(request, 'practice.html', {})


# *** Transactions -- (transactions refers to a set of operations that will occur all together or not at all):
# * There are two ways to handle a transaction, either we could make the whole method a transaction, or a part of the code.

#* This decorator(annotation) will make the whole method a transaction
# @transaction.atomic
# def practice(request):
#     #* We could perform a transaction on a specific code:
#     with transaction.atomic():
#         order = Order()
#         order.customer_id = 1
#         order.save()

#         order_item = OrderItem()
#         order_item.order = order
#         order_item.product_id = -1
#         order_item.quantity = 1
#         order_item.unit_price = 4.99
#         order_item.save()

#     return render(request, 'practice.html', {})


# *** Executing RAW sql query:
def practice(request):
    # * There are two ways to execute raw query : 
    # query_set = Product.objects.raw("select * from store_product")

    # * Another way is to : this works even if we don't have existing model for it:
    with connection.cursor() as cursor:
        cursor.execute('select * from customer')
        query_set = cursor.fetchall()

    # * Lastly, we could call stored procedure: 
    # with connection.cursor() as cursor:
    #     cursor.callproc()
    
    return render(request, 'practice.html', {'results': list(query_set)})