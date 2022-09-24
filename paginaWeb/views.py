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


#Registros clientes
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
            #editamos primero la contraseña y su rol
            usuarios = Usuarios.objects.get(id_correo=request.POST['correo'])
            usuarios.contrasena = request.POST['contrasena']
            usuarios.roles = Roles.objects.get(pk=request.POST['rol'])
            usuarios.save()


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

#hubo problemas con el nombre, luego se cambian
def listarClientes(request):

    q = Clientes.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/clientes/listarUsuarios.html', contexto)

def buscarClienteEditar(request, id):

    q = Clientes.objects.get(pk = id)

    contexto = {'clientes': q}

    return render(request, 'run/clientes/editarClientes.html', contexto)


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
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'La marca esta vinculada a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:lsit_marcas')
        else:
            messages.error(request, f'Hubo un problema al eliminar una marca: {e}')
            return redirect('paginaWeb:lsit_marcas')


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

#Usuarios
def formUsuarios(request):
    return render(request, 'run/usuarios/usuariosForm.html')

def listarUsuarios(request):

    q = Usuarios.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/usuarios/listarUsuarios.html', contexto)

def addUsuarios(request):
    if request.method == 'POST':
        try:
            q = Usuarios(
                id_correo = request.POST['correo'],
                contrasena = request.POST['contrasena'],
                roles = Roles.objects.get(pk=request.POST['rol'])
            )
            q.save()
            return redirect('paginaWeb:list_usuarios')
        except Exception as e: 
            messages.error(request, f'Hubo un problema al agregar usuario: {e}')
            return redirect('paginaWeb:list_usuarios')
    else:
        messages.warning(request, 'Estás intentado hackear al ganador del SENASOFT? En serio?')
        return redirect('paginaWeb:list_usuarios')

def deleteUsuarios(request, id):
    try:
        usuario = Usuarios.objects.get(id_correo = id)
        usuario.delete()
        messages.success(request, 'usuario eliminado correctamente')
        return redirect('paginaWeb:list_usuarios')
    except Exception as e: 
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'El usuario esta vinculado a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_usuarios')
        else:
            messages.error(request, f'Hubo un problema al eliminar un usuario: {e}')
            return redirect('paginaWeb:list_usuarios')


def updateUsuariosForm(request, id):

    q = Usuarios.objects.get(pk = id)

    contexto = {'usuarios': q}

    return render(request, 'run/usuarios/editarUsuarios.html', contexto)

def updateUsuarios(request):
    
    if request.method == "POST":
        try:
    
            usuarios = Usuarios.objects.get(id_correo=request.POST['correo'])
            #que error tan raro, si le pongo al input de correo el atributo disabled, no me permite gestionarlo aqui... el atributo lo corrompe o no lo se...
            
            usuarios.contrasena = request.POST['contrasena']
            usuarios.roles = Roles.objects.get(pk=request.POST['rol'])

            usuarios.save()
            messages.success(request, 'usuario actualizado correctamente')
            return redirect('paginaWeb:list_usuarios')  

        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al intentar editar un usuario: {e}')
            return redirect('paginaWeb:list_usuarios')  
    else: 
        messages.warning(request, 'Estás intentado hackear al ganador del SENASOFT? En serio?')
        return redirect('paginaWeb:list_usuarios')

#Empleados
def formEmpleados(request):
    return render(request, 'run/empleados/empleadosForm.html')

def listarEmpleados(request):

    q = Empleados.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/empleados/listarEmpleados.html', contexto)

def addEmpleados(request):
    if request.method == 'POST':
        try:    
            CoExistente = Usuarios.objects.filter(id_correo=request.POST['Correo'])
            ceduExistente = Empleados.objects.filter(id_empleado= request.POST['id_empleado'])
            if CoExistente:
                messages.error(request, "Correo ya registrado, ingrese uno diferente por favor")
                return render(request, 'run/empleados/empleadosForm.html')
            elif ceduExistente:
                messages.error(request, "cedula ya registrada, ingrese una diferente por favor")
                return render(request, 'run/empleados/empleadosForm.html')
            else:
                usuarioContrasena = Usuarios(
                    id_correo = request.POST['Correo'], 
                    contrasena = request.POST['contrasena'], 
                    roles = Roles.objects.get(pk=2)
                )
                usuarioContrasena.save()
                q = Empleados(
                    id_empleado = request.POST['id_empleado'],
                    nombre_empleado = request.POST['nombre_empleado'],
                    apellido_empleado = request.POST['apellido_empleado'],
                    celular_empleado = request.POST['celular_empleado'],
                    fecha_nacimiento = request.POST['fecha_nacimiento'],
                    direccion_empleado = request.POST['direccion_empleado'],
                    eps = request.POST['eps'],
                    correo = Usuarios.objects.get(pk = request.POST['Correo'])) #aqui cambia la cosa)
                q.save()
                messages.success(request, "Empleado registrado exitosamente")
                return redirect('paginaWeb:list_empleados')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return render(request, 'run/empleados/empleadosForm.html')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return redirect('paginaWeb:list_empleados')

def deleteEmpleados(request, id):
    try:
        empleado = Empleados.objects.get(id_empleado = id)
        usuario = Usuarios.objects.get(id_correo = empleado.correo)
        empleado.delete()
        usuario.delete()
        messages.success(request, 'empleado eliminado correctamente')
        return redirect('paginaWeb:list_empleados')
    except Exception as e: 
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'El empleado esta vinculado a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_empleados')
        else:
            messages.error(request, f'Hubo un problema al eliminar un empleado: {e}')
            return redirect('paginaWeb:list_empleados')


def updateEmpleadosForm(request, id):

    q = Empleados.objects.get(pk = id)

    contexto = {'empleados': q}

    return render(request, 'run/empleados/editarEmpleados.html', contexto)

def updateEmpleados(request):
    
    if request.method == "POST":
        try:
            empleado = Empleados.objects.get(pk=request.POST['id_empleado'])
            #editamos primero la contraseña y su rol
            usuarios = Usuarios.objects.get(id_correo=request.POST['correo'])
            usuarios.contrasena = request.POST['contrasena']
            usuarios.roles = Roles.objects.get(pk=request.POST['rol'])
            usuarios.save()
 
            empleado.nombre_empleado = request.POST['nombre_empleado']
            empleado.apellido_empleado = request.POST['apellido_empleado']
            empleado.celular_empleado = request.POST['celular_empleado']
            empleado.direccion_empleado = request.POST['direccion_empleado']
            empleado.eps = request.POST['eps']

            
            empleado.save()
            messages.success(request, "Actualizado correctamente")
            return redirect('paginaWeb:list_empleados')
        except Exception as e:
            messages.error(request, f"Hubo un error al momento de actualizar: {e}")
            return redirect('paginaWeb:list_empleados')

    else:
        messages.warning(request, "No sabemos por donde se esta metiendo pero no puedes avanzar, puerco")
        return redirect('paginaWeb:list_empleados')

#Ventas
# def formVentas(request):
#     return render(request, 'run/ventas/ventasForm.html')

# def listarVentas(request):

#     q = Ventas.objects.all()

#     contexto = {'datos': q}

#     return render(request, 'run/ventas/listarVentas.html', contexto)

# def addVentas(request):
#     if request.method == 'POST':
#         try:    
#             CoExistente = Usuarios.objects.filter(id_correo=request.POST['Correo'])
#             ventaExistente = Ventas.objects.filter(id_empleado= request.POST['id_empleado'])
#             if ventaExistente:
#                 messages.error(request, "Venta ya registrada, ingrese una diferente por favor")
#                 return render(request, 'run/ventas/ventasForm.html')
#             else:
#                 usuarioContrasena = Usuarios(
#                     id_correo = request.POST['Correo'], 
#                     contrasena = request.POST['contrasena'], 
#                     roles = Roles.objects.get(pk=2)
#                 )
#                 usuarioContrasena.save()
#                 q = Empleados(
#                     id_empleado = request.POST['id_empleado'],
#                     nombre_empleado = request.POST['nombre_empleado'],
#                     apellido_empleado = request.POST['apellido_empleado'],
#                     celular_empleado = request.POST['celular_empleado'],
#                     fecha_nacimiento = request.POST['fecha_nacimiento'],
#                     direccion_empleado = request.POST['direccion_empleado'],
#                     eps = request.POST['eps'],
#                     correo = Usuarios.objects.get(pk = request.POST['Correo'])) #aqui cambia la cosa)
#                 q.save()
#                 messages.success(request, "Empleado registrado exitosamente")
#                 return redirect('paginaWeb:list_empleados')
#         except Exception as e:
#             messages.error(request, f"Hubo un error en el proceso de registro: {e}")
#             return render(request, 'run/empleados/empleadosForm.html')
#     else:
#         messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
#         return redirect('paginaWeb:list_empleados')

# def deleteEmpleados(request, id):
#     try:
#         empleado = Empleados.objects.get(id_empleado = id)
#         usuario = Usuarios.objects.get(id_correo = empleado.correo)
#         empleado.delete()
#         usuario.delete()
#         messages.success(request, 'empleado eliminado correctamente')
#         return redirect('paginaWeb:list_empleados')
#     except Exception as e: 
#         if str(e) == "FOREIGN KEY constraint failed":
#             messages.error(request, f'El empleado esta vinculado a otros registros, eliminelos y luego vuelva a intentarlo')
#             return redirect('paginaWeb:list_empleados')
#         else:
#             messages.error(request, f'Hubo un problema al eliminar un empleado: {e}')
#             return redirect('paginaWeb:list_empleados')


# def updateEmpleadosForm(request, id):

#     q = Empleados.objects.get(pk = id)

#     contexto = {'empleados': q}

#     return render(request, 'run/empleados/editarEmpleados.html', contexto)

# def updateEmpleados(request):
    
#     if request.method == "POST":
#         try:
#             empleado = Empleados.objects.get(pk=request.POST['id_empleado'])
#             #editamos primero la contraseña y su rol
#             usuarios = Usuarios.objects.get(id_correo=request.POST['correo'])
#             usuarios.contrasena = request.POST['contrasena']
#             usuarios.roles = Roles.objects.get(pk=request.POST['rol'])
#             usuarios.save()
 
#             empleado.nombre_empleado = request.POST['nombre_empleado']
#             empleado.apellido_empleado = request.POST['apellido_empleado']
#             empleado.celular_empleado = request.POST['celular_empleado']
#             empleado.direccion_empleado = request.POST['direccion_empleado']
#             empleado.eps = request.POST['eps']

            
#             empleado.save()
#             messages.success(request, "Actualizado correctamente")
#             return redirect('paginaWeb:list_empleados')
#         except Exception as e:
#             messages.error(request, f"Hubo un error al momento de actualizar: {e}")
#             return redirect('paginaWeb:list_empleados')

#     else:
#         messages.warning(request, "No sabemos por donde se esta metiendo pero no puedes avanzar, puerco")
#         return redirect('paginaWeb:list_empleados')

#Pedidos
def formPedidos(request):

    q = Clientes.objects.all()

    contexto = {'clientes': q}


    return render(request, 'run/pedidos/pedidosForm.html', contexto)

def listarPedidos(request):

    q = Pedidos.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/pedidos/listarPedidos.html', contexto)

def addPedidos(request):
    if request.method == 'POST':
        try:    
            CoExistente = Clientes.objects.filter(id_cliente=request.POST['cliente'])
            pediExistente = Pedidos.objects.filter(id_pedido= request.POST['id_pedido'])
            if not CoExistente:
                messages.error(request, "usuario no encontrado, ingrese uno diferente por favor")
                return render(request, 'run/pedidos/pedidosForm.html')
            elif pediExistente:
                messages.error(request, "id de pedido ya registrada, ingrese una diferente por favor")
                return render(request, 'run/pedidos/pedidosForm.html')
            else:
                q = Pedidos(
                    id_pedido = request.POST['id_pedido'],
                    cliente = Clientes.objects.get(pk = request.POST['cliente']))
                
                q.save()
                messages.success(request, "Pedido registrado exitosamente")
                return redirect('paginaWeb:list_pedidos')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:form_pedidos')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return redirect('paginaWeb:list_pedidos')

def deletePedidos(request, id):
    try:
        pedido = Pedidos.objects.get(pk= id)
        pedido.delete()
        messages.success(request, 'pedido eliminado correctamente')
        return redirect('paginaWeb:list_pedidos')
    except Exception as e: 
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'El empleado esta vinculado a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_pedidos')
        else:
            messages.error(request, f'Hubo un problema al eliminar un pedido: {e}')
            return redirect('paginaWeb:list_pedidos')


def updatePedidosForm(request, id):

    q = Pedidos.objects.get(pk = id)
    c = Clientes.objects.all()
    contexto = {'pedidos': q, 'clientes': c}

    return render(request, 'run/pedidos/editarPedidos.html', contexto)

def updatePedidos(request):
    
    if request.method == "POST":
        try: 
            cliente = Clientes.objects.get(pk=request.POST['id_cliente'])
            #editamos primero la contraseña y su rol
            pedido = Pedidos.objects.get(id_pedido=request.POST['id_pedido'])
            pedido.cliente = cliente
            pedido.save()

            messages.success(request, "Actualizado correctamente")
            return redirect('paginaWeb:list_pedidos')
        except Exception as e:
            messages.error(request, f"Hubo un error al momento de actualizar: {e}")
            return redirect('paginaWeb:list_pedidos')

    else:
        messages.warning(request, "No sabemos por donde se esta metiendo pero no puedes avanzar, puerco")
        return redirect('paginaWeb:list_pedidos')

