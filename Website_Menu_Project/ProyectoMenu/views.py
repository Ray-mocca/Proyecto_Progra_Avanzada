from django import forms
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Max
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from .forms import ProductForm, BakeryClassForm, CustomUserCreationForm, CustomerForm, ProfileForm
from .models import Product, BakeryClass, Cart, Purchase, Customer



# Create your views here.
#Register view

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Bienvenido a Panadería Deliciosa. Por favor, completa tu perfil.')
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
    

#Update Profile view

@login_required
def profile(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=customer)
    return render(request, 'paginas/profile.html', {'form': form})

#------------ paginas ----------------#

def inicio(request):
    featured_products = Product.objects.filter(featured=True)[:3]
    return render(request, 'paginas/inicio.html', {'featured_products': featured_products})

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

@login_required
@staff_member_required
def manage_products(request):
    print("View function hit!")
    products = Product.objects.all()
    return render(request, 'paginas/productos.html', {'products': products})
    

@login_required
@staff_member_required
def add_product(request):
    form = ProductForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('manage_products')
        
    return render(request, 'paginas/add_product.html', {'form': form})

@login_required
@staff_member_required
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, 'Product deleted successfully.')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
    return redirect('manage_products')

@login_required
@staff_member_required
def add_bakery_class(request):
    if request.method == 'POST':
        form = BakeryClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clase añadida correctamente.')
            return redirect('bakery_classes')
    else:
        form = BakeryClassForm()
    return render(request, 'paginas/add_bakery_class.html', {'form': form})

# ------------ Purchase section ----------------#
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart.quantity += 1
        cart.save()
    
    return redirect('view_cart')
    
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(float(item.product.price) * item.quantity for item in cart_items)
    return render(request, 'paginas/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def update_cart(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            quantity_key = f'quantity_{item.product.id}'
            if quantity_key in request.POST:
                try:
                    new_quantity = int(request.POST[quantity_key])
                    if new_quantity > 0:
                        item.quantity = new_quantity
                        item.save()
                    else:
                        item.delete()
                except ValueError:
                    messages.error(request, 'Invalid quantity provided.')
    return redirect('view_cart')


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    customer, created = Customer.objects.get_or_create(user=request.user)
    total_price = sum(float(item.product.price) * item.quantity for item in cart_items)
    #Numero Orden de compra
    last_order = Purchase.objects.aggregate(Max('order_id'))
    if last_order['order_id__max'] is not None:
        new_order_id = last_order['order_id__max'] + 1
    else:
        new_order_id = 1
    
    if request.method == 'POST':
        order_details = []
        for item in cart_items:
            Purchase.objects.create(
                customer=request.user.customer,
                product=item.product,
                quantity=item.quantity,
                order_id=new_order_id
            )
            order_details.append(f"{item.product.name} - Quantity: {item.quantity}")
        cart_items.delete()

        store_email = "raymondsan95@gmail.com"
        customer_address = customer.address if customer.address else "N/A"
        customer_phone = customer.phone_number if customer.phone_number else "N/A"
        
        #Pasar detalles del pedido al frontend
        context = {
            'order_id': new_order_id,
            'order_details': order_details,
            'total_price': total_price,
            'store_email': store_email,
            'customer_address': customer_address,
            'customer_phone': customer_phone,
        }
        return render(request, 'paginas/checkout_complete.html', context)
    
    return render(request, 'paginas/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def purchase_history(request):
    purchases = Purchase.objects.filter(customer=request.user.customer)
    return render(request, 'paginas/purchase_history.html', {'purchases': purchases})

#------------ Tabla de pedidos -----------
@login_required
@staff_member_required
def orders_table(request):
    if not request.user.is_staff:
        return redirect('inicio')
    orders = Purchase.objects.all().order_by('order_id')
    return render(request, 'paginas/tabla_pedidos.html', {'orders': orders})

### View to change password
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
@login_required
def change_password(request):
    print("Request method:", request.method)
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
        else:
            print("Form errors:", form.errors)
        # Si el formulario no es válido, vuelve a mostrar el formulario con errores
        return render(request, 'paginas/change_password.html', {'form': form})
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    print("Rendering template")
    # Asegúrate de que siempre se devuelve una respuesta
    return render(request, 'paginas/change_password.html', {'form': form})


