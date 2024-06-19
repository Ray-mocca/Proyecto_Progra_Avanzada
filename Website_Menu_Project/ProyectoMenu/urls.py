from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('contacto/', views.contacto, name='contacto'),
    path('servicios/', views.servicios, name='servicios'),
    path('catering/', views.catering, name='catering'),
    path('delivery/', views.delivery, name='delivery'),
    path('baking_classes', views.baking_classes, name='baking_classes'),
    path('custom_cakes', views.custom_cakes, name='custom_cakes')
]