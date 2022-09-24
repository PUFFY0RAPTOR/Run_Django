from email import message
from urllib import request
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *


# Create your views here.
def index(request):
    return render(request, 'run/index.html')


#Login
def loginForm(request):
    return render(request, 'run/login/login.html')

def login(request):
    if request.method == 'POST':
        try:
            correo = request.POST['email']
            passw = request.POST['passw']

            q = Usuarios.objects.get(id_correo = correo, contrasena = passw)

            request.session['auth'] = [q.id_correo, q.contrasena]

            messages.success(request, 'Bienvenido!!')
            return redirect('paginaWeb:index')
        except Exception as e:
            messages.error(request, f'Un error ha ocurrido durante el logueo... {e}')
            return redirect('paginaWeb:index')
    else:
        messages.warning(request, '¿Qué estás haciendo?')
        return redirect('paginaWeb:index')


def logout(request):
    try:
        del request.session['auth']
        messages.success(request, 'Sesión cerrada correctamente')

    except Exception as e:
        messages.error(request, f"Ocurrió un error, intente de nuevo...")
    
    return redirect('paginaWeb:index')


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

def deleteMarcas(request, id):
    try:
        marca = Marcas.objects.get(pk = id)
        marca.delete()
        messages.success(request, 'Marca eliminada correctamente')
        return redirect('paginaWeb:list_marcas')
    except Exception as e: 
        messages.error(request, f'Hubo un problema al eliminar una marca: {e}')

def updateMarcasForm(request, id):

    q = Marcas.objects.get(pk = id)

    contexto = {'marcas': q}

    return render(request, 'run/marcas/editarMarcas.html', contexto)

def updateMarcas(request):
    
    if request.method == "POST":
        try:
            marcas = Marcas.objects.get(pk = request.POST['code'])
            
            marcas.nombre_marca = request.POST['marcas']
            marcas.save()
            messages.success(request, 'Marca actualizada correctamente')
            return redirect('paginaWeb:list_marcas')  
            
        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al intentar editar una marca: {e}')
            return redirect('paginaWeb:list_marcas')  
    else: 
        messages.warning(request, 'Estás intentado hackear al ganador del SENASOFT? En serio?')
        return redirect('paginaWeb:list_marcas')

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

    q = Productos.objects.all()

    contexto = {'productos': q}

    return render(request, 'run/inventario/listarInventario.html', contexto)

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
        return redirect('paginaWeb:list_inv')
        
    except Exception as e:
        return HttpResponse("Error: "+ e)

def deleteInventario(request, id):
    try:
        producto = Productos.objects.get(pk=id)
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente')
        return redirect('paginaWeb:list_inv')
    except Exception as e:
        messages.error(request, f'Hubo un problema al intentareliminar : {e}')
        return redirect('paginaWeb:list_inv')

def updateInventarioForm(request, id):

    q = Productos.objects.get(pk=id)
    m = Marcas.objects.all()

    contexto = {'productos': q, 'dataMarcas': m}
    
    return render(request, 'run/inventario/editarInventario.html', contexto)

def updateInventario(request):
    if request.method == "POST":
        try:
            productos = Productos.objects.get(pk = request.POST['codigo'])

            productos.nombre_producto = request.POST['nombreRes']
            productos.stock = request.POST['stock']
            productos.precio = request.POST['precio']
            productos.marca = Marcas.objects.get(pk = request.POST['marca'])
            productos.descripcion = request.POST['descripcion']
            productos.save()
            messages.success(request, 'Producto correctamente editado')
            return redirect('paginaWeb:list_inv')

        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al intenar editar: {e}')
            return redirect('paginaWeb:list_inv')
    else:
        messages.warning(request, 'Estás intentado hackear al ganador del SENASOFT? En serio?')
        return redirect('paginaWeb:list_inv')

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


#Admin - Roles
def listRoles(request):

    q = Roles.objects.all()

    contexto = {'roles': q}

    return render(request, 'run/listarRoles.html', contexto)

def regRolesForm(request):
    return render(request, 'run/registros/registroRoles.html')

def rolRegistro(request):

    if request.method == 'POST':
        try:
            q = Roles(
                id_roles = request.POST['idRol'],
                nombre_rol = request.POST['nameRol'],
                descripcion = request.POST['descripcion'],
            )
            q.save()
            messages.success(request, 'Rol añadido correctamente')
            return redirect('paginaWeb:list_roles')

        except Exception as e:
            messages.error(request, f'Hubo un error al intentar añadir un rol: {e}')
            return redirect('paginaWeb:list_roles')
    else: 
        messages.warning(request, 'Estás intentado hackear al ganador del SENASOFT? En serio?')
        return redirect('paginaWeb:list_roles')

def deleteRol(request, id):
    try:
        rol = Roles.objects.get(pk=id)
        rol.delete()
        messages.success(request, 'Rol eliminado correctamente')
        return redirect('paginaWeb:list_roles')
    except Exception as e:
        messages.error(request, f'Hubo un error al intentar eliminar un rol: {e}')
        return redirect('paginaWeb:list_roles')

def updateRolForm(request, id):

    q = Roles.objects.get(pk=id)

    contexto = {'roles':q}

    return render(request, 'run/roles/editarRoles.html', contexto)

def updateRol(request):
    if request.method == 'POST':
        try:
            roles = Roles.objects.get(pk = request.POST['idRol'])

            roles.nombre_rol = request.POST['nameRol']
            roles.descripcion = request.POST['descripcion']
            roles.save()
            messages.success(request, 'Rol actualizado correctamente')
            return redirect('paginaWeb:list_roles')
        except Exception as e:
            messages.error(request, f'Hubo un error al intentar actualizar un rol: {e}')
            return redirect('paginaWeb:list_roles')
    else:
        messages.warning(request, '¿Qué estás intentando?')
        return redirect('paginaWeb:list_roles')