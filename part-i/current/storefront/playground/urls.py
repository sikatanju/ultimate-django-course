from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('practice/', views.practice),
    path('crud/', views.django_crud),
]
