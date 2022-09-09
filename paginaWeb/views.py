from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *


# Create your views here.
def index(request):
    return render(request, 'run/index.html')

def login(request):
    return render(request, 'run/login/login.html')


#Registros usuarios
def registro(request):
    return render(request, 'run/registros/registro.html')

def listarUsuarios(request):

    q = Clientes.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/clientes/listarUsuarios.html', contexto)


#Repuestos
def listarRepuestos(request):

    q = Productos.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/repuestos/listarRepuestos.html', contexto)


#Compras
def verProductos(request):
    return render(request, 'run/compras/compras.html')


#Inventario
def registroInventario(request):
    return render(request, 'run/registros/registroInventario.html')

def listarInventario(request):
    return render(request, 'run/inventario/listarInventario.html')


#Ayuda
def ayuda(request):
    return render(request, 'run/ayuda/ayuda.html')


#Marcas 
def marcas(request):
    return render(request, 'run/marcas/marcas.html')


#Carrito
def carritoCompras(request):

    q = Productos.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/carritoCompras.html', contexto)

