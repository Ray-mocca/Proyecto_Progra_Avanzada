from django.urls import path, include
from . import views
from .views import CustomLoginView, register, change_password
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
    path('manage_products/', views.manage_products, name='manage_products'),
    path('add_bakery_class/', views.add_bakery_class, name='add_bakery_class'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('about_us/', views.about_us, name='about_us'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.Custom_Logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    #compras

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('orders/', views.orders_table, name='tabla_pedidos'),
    path('change-password/', views.change_password, name='change_password'),
]
