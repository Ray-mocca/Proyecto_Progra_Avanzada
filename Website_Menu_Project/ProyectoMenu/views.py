from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Product, BakeryClass
from .forms import ProductForm, BakeryClassForm
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseForbidden


# Create your views here.
#Register view

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = CustomUserCreationForm()
    return render(request, 'paginas/register.html', {'form': form})

#Login View
class CustomLoginView(LoginView):
    template_name = 'paginas/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('inicio')
    
    class CustomAuthenticationForm(AuthenticationForm):
        username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

#Logout view

def Custom_Logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('inicio')
    else:
        return HttpResponseForbidden("Invalid request method")

def inicio(request):
    return render(request, 'paginas/inicio.html')

def productos(request):
    products = Product.objects.all()
    return render(request, 'paginas/productos.html', {'products': products})

def servicios(request):
    return render(request, 'paginas/servicios.html')

def contacto(request):
    return render(request, 'paginas/contacto.html')

def catering(request):
    return render(request, 'paginas/catering.html')

def delivery(request):
    return render(request, 'paginas/delivery.html')

def bakery_classes(request):
    classes = BakeryClass.objects.all()
    return render(request, 'paginas/bakery_classes.html', {'bakery_classes': classes})

def custom_cakes(request):
    return render(request, 'paginas/custom_cakes.html')

def about_us(request):
    return render(request, 'paginas/about_us.html')


#--------------------- Autenticación de staff y administrador ---------------#
#def is_admin(user):
    #return user.is_autheticated

def check_superuser(user):
    return user.is_superuser

#---------------------- Vista de añadir productos y clases ----------------------#

@user_passes_test(check_superuser)
def manage_products(request):
    print("View function hit!")
    products = Product.objects.all()
    return render(request, 'manage_products.html', {'products': products})
    return render(request, 'base.html')

@user_passes_test(check_superuser)
def add_product(request):
    form = ProductForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('manage_products')
        
    return render(request, 'paginas/add_product.html', {'form': form})

@user_passes_test(check_superuser)
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, 'Product deleted successfully.')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
    return redirect('manage_products')
    return render(request, 'base.html')

@user_passes_test(check_superuser)
def add_bakery_class(request):
    if request.method == 'POST':
        form = BakeryClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bakery_classes')
    else:
        form = BakeryClassForm()
    return render(request, 'paginas/add_bakery_class.html', {'form': form})
    return render(request, 'base.html')