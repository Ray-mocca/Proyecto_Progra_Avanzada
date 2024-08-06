from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Product, Cart, CateringRequest, CustomCakeRequest, DeliveryRequest, BakeryClass, Customer, Purchase, PurchaseHistory, Student, Enrollment

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CateringRequest)
admin.site.register(CustomCakeRequest)
admin.site.register(DeliveryRequest)
admin.site.register(BakeryClass)
admin.site.register(Customer)
admin.site.register(Purchase)
admin.site.register(PurchaseHistory)
admin.site.register(Student)
admin.site.register(Enrollment)
