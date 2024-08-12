from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
# from pprint import pprint

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
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)

#* Either we could do this, if only we're using the urls from router:
# urlpatterns = router.urls

#* Otherwise, if we have other url pattern we have to specify, what we could do is:

urlpatterns = [
    path('', include(router.urls)),
]