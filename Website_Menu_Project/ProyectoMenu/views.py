from django.shortcuts import render

# Create your views here.


def inicio(request):
    return render(request, 'paginas/inicio.html')
    return render(request, 'base.html')