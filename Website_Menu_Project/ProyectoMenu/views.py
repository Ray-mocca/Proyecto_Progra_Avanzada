from django.shortcuts import render

# Create your views here.


def inicio(request):
    return render(request, 'paginas/inicio.html')
    return render(request, 'base.html')

def productos(request):
    return render(request, 'paginas/productos.html')
    return render(request, 'base.html')
    
def servicios(request):
    return render(request, 'paginas/servicios.html')
    return render(request, 'base.html')
def contacto(request):
    return render(request, 'paginas/contacto.html')
    return render(request, 'base.html')