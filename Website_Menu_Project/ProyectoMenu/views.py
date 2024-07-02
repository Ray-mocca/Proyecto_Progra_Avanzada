from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Product, BakeryClass
from .forms import ProductForm, BakeryClassForm

# Create your views here.


def inicio(request):
    return render(request, 'paginas/inicio.html')
    return render(request, 'base.html')

def productos(request):
    products = Product.objects.all()
    return render(request, 'paginas/productos.html', {'products': products})
    return render(request, 'base.html')
    
def servicios(request):
    return render(request, 'paginas/servicios.html')
    return render(request, 'base.html')

def contacto(request):
    return render(request, 'paginas/contacto.html')
    return render(request, 'base.html')

def catering(request):
    return render(request, 'paginas/catering.html')
    return render(request, 'base.html')

def delivery(request):
    return render(request, 'paginas/delivery.html')
    return render(request, 'base.html')

def bakery_classes(request):
    classes = BakeryClass.objects.all()
    return render(request, 'paginas/bakery_classes.html', {'bakery_classes': classes})
    return render(request, 'base.html')

def custom_cakes(request):
    return render(request, 'paginas/custom_cakes.html')
    return render(request, 'base.html')


#--------------------- Autenticación de staff y administrador ---------------#
#def is_admin(user):
    #return user.is_autheticated

def check_superuser(user):
    return user.is_superuser

#---------------------- Vista de añadir productos y clases ----------------------#

@user_passes_test(check_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductForm()
    return render(request, 'paginas/add_product.html', {'form': form})
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

@user_passes_test(check_superuser)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('productos')
    return render(request, 'paginas/delete_product.html', {'product': product})