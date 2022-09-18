from email import message
from django.urls import reverse
from django.contrib import messages
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

def guardarCliente(request):
    if request.method == 'POST':
        try:    
            CoExistente = Usuarios.objects.filter(id_correo=request.POST['Correo'])
            ceduExistente = Clientes.objects.filter(id_cliente= request.POST['Id'])
            if CoExistente:
                messages.error(request, "Correo ya registrado, ingrese uno diferente por favor")
                return render(request, 'run/registros/registro.html')
            elif ceduExistente:
                messages.error(request, "cedula ya registrada, ingrese una diferente por favor")
                return render(request, 'run/registros/registro.html')
            else:
                usuarioContrasena = Usuarios(
                    id_correo = request.POST['Correo'], 
                    contrasena = request.POST['contrasena'], 
                    roles = Roles.objects.get(pk=1)
                )
                usuarioContrasena.save()
                q = Clientes(
                    id_cliente = request.POST['Id'],
                    nombre_cliente = request.POST['Nombre'],
                    apellido_cliente = request.POST['Apellidos'],
                    celular_cliente = request.POST['Celular'],
                    fecha_nacimiento = request.POST['FechaNacim'],
                    direccion = request.POST['Direccion'],
                    correo = Usuarios.objects.get(pk = request.POST['Correo'])) #aqui cambia la cosa)
                q.save()
                #return render(request, 'run/login/login.html')
                messages.success(request, "Usuario registrado exitosamente")
                return redirect('paginaWeb:list_usu')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return render(request, 'run/registros/registro.html')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return render(request, 'run/index.html')

def eliminarCliente(request, id):
    try:
        usuario = Clientes.objects.get(pk=id)
        usuarioCorreo = Usuarios.objects.get(pk=usuario.correo)
        usuario.delete()
        usuarioCorreo.delete()
        messages.success(request, "Eliminado correctamente")
        return redirect ('paginaWeb:list_usu')
    except Exception as e:
        messages.error(request, f"Hubo un error al eliminar el usuario : {e}")
        return redirect ('paginaWeb:list_usu')
    

def updateCliente(request):
    if request.method == "POST":
        try:
            cliente = Clientes.objects.get(pk=request.POST['cedula'])
            
            cliente.nombre_cliente = request.POST['nombre']
            cliente.apellido_cliente = request.POST['apellidos']
            cliente.celular_cliente = request.POST['telefono']
            cliente.direccion = request.POST['direccion']
            
            cliente.save()
            messages.success(request, "Actualizado correctamente")
            return redirect('paginaWeb:list_usu')
        except Exception as e:
            messages.error(request, f"Hubo un error al momento de actualizar: {e}")
            return redirect('paginaWeb:list_usu')

    else:
        messages.warning(request, "No sabemos por donde se esta metiendo pero no puedes avanzar, puerco")
        return redirect('paginaWeb:list_usu')


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
    q = Marcas.objects.all()

    contexto = {'dataMarcas': q}

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

