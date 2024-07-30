from django.urls import path
from . import views
from .views import CustomLoginView, register
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('contacto/', views.contacto, name='contacto'),
    path('servicios/', views.servicios, name='servicios'),
    path('catering/', views.catering, name='catering'),
    path('delivery/', views.delivery, name='delivery'),
    path('bakery_classes/', views.bakery_classes, name='bakery_classes'),
    path('custom_cakes/', views.custom_cakes, name='custom_cakes'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_bakery_class/', views.add_bakery_class, name='add_bakery_class'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('about_us/', views.about_us, name='about_us'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.Custom_Logout, name='logout'),
]
