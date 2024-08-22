from django.urls import path, include
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from pprint import pprint

from . import views

"""
* There is another router we could use, that comes with additional features, which is DefaultRouter()
* Now, if we go to this url '/store/products.json' we get all the products in json format
* Also, if we go to '/store/', we get two urls for products & collections like given below:
{
    "products": "http://localhost:8000/store/products/",
    "collections": "http://localhost:8000/store/collections/"
}
"""


# router = SimpleRouter()
router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet)

router.register('products', views.ProductViewSet, basename='products')
# router.register('reviews', views.Review)

router.register('carts', views.CartViewSet, basename='carts')

router.register('customers', views.CustomerViewSet, basename='customers')


review_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
review_router.register(r'reviews', views.ReviewViewSet, basename='product-reviews')

cartitem_router = routers.NestedDefaultRouter(router, r'carts', lookup='cart')
cartitem_router.register('items', views.CartItemViewSet, basename='cart-items')


# pprint(review_router.urls)

#* Either we could do this, if only we're using the urls from router:
# urlpatterns = router.urls + review_router.urls

#* Otherwise, if we have other url pattern we have to specify, what we could do is:

urlpatterns = [
    path('', include(router.urls)),
    path('', include(review_router.urls)),
    path('', include(cartitem_router.urls)),
]