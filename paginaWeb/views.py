from django.urls import reverse
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


#Marcas
def formMarcas(request):
    return render(request, 'run/marcas/marcasForm.html')

def listarMarcas(request):

    q = Marcas.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/marcas/listarMarcas.html', contexto)

def addMarcas(request):
    try:
        q = Marcas(
            id_marca = request.POST['code'],
            nombre_marca = request.POST['marcas'],
        )
        q.save()
        return redirect('paginaWeb:list_marcas')

    except Exception as e: 
        return HttpResponse(e)


#Compras
def verProductos(request):
    return render(request, 'run/compras/compras.html')


#Inventario
def registroInventario(request):
    q = Marcas.objects.all()

    contexto = {'dataMarcas': q}
    #print(contexto)

    return render(request, 'run/registros/registroInventario.html', contexto)


def listarInventario(request):
    return render(request, 'run/inventario/listarInventario.html')

def crearInventario(request): 
    try:
        q = Productos(
            id_producto = request.POST['codigo'],
            nombre_producto = request.POST['nombreRes'],
            stock = request.POST['stock'],
            precio = request.POST['precio'],
            marca = Marcas.objects.get(pk = request.POST['marca']),
            descripcion = request.POST['descripcion'],
        ) 
        q.save()
        return redirect('paginaWeb:list_rep')
        
    except Exception as e:
        return HttpResponse("Error: "+ e)


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

