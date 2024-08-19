from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)


class CateringRequest(models.Model):
    client_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255)
    requested_items = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Catering Request from {self.client_name} ({self.created_at})"

class CustomCakeRequest(models.Model):
    client_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    description = models.TextField()
    price_inquiry = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Custom Cake Request from {self.client_name} ({self.created_at})"

class DeliveryRequest(models.Model):
    client_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255)
    requested_items = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery Request from {self.client_name} ({self.created_at})"

class BakeryClass(models.Model):
    CLASS_LEVELS =[
        ('Beginner', 'Beginner'),
        ('Mid', 'Mid'),
        ('Advanced', 'Advanced'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    class_level = models.CharField(max_length=20, choices=CLASS_LEVELS)

    def __str__(self):
        return f"{self.class_level} Class: {self.name}"

class Customer(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{9,15}$', message='Enter a valid phone number.')])
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name})"

class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    order_id = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.customer.name} purchased {self.quantity} {self.product.name} ({self.purchase_date})"
    
class PurchaseHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)                                 

class Student(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{9,15}$', message='Enter a valid phone number.')])

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    bakery_class = models.ForeignKey(BakeryClass, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enrollment of {self.student.name} in {self.bakery_class.name} on {self.enrollment_date}"
    
