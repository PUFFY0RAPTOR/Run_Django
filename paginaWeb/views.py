from email import message
from urllib import request
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
#from .cryp import claveEncriptada

#almacenamiento de archivos o fotos
from django.core.files.storage import FileSystemStorage
#---------------------------------------------------------------- Decoradores ----------------------------------------------------------------

#A = Administrador, E = Empleado, C = CLiente

#Decorador para controlar la entrada desde las rutas
def decoradorPermitirAE(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth and (auth[2] == 3 or auth[2] == 2):
            return funcionPrincipal(request, *args, **kwargs)
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')
    return autenticar 

#NO puede entrar los administradores ni tampoco los empleados ni los clientes, nadie logueado
def decoradorDenegarAEC(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')   
        else:
            return funcionPrincipal(request, *args, **kwargs) #Ahorrar codigo explicar a sebas
    return autenticar 

#No puede entrar a menos que este logueado
def decoradorPermitirAEC(funcionPrincipal): 
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth:
            return funcionPrincipal(request, *args, **kwargs) #Ahorrar codigo explicar a sebas
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')   
            
    return autenticar 

#Solo un administrador puede entrar
def decoradorPermitirA(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth and (auth[2] == 3):
            return funcionPrincipal(request, *args, **kwargs)
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index') 
    return autenticar

#Solo un Cliente puede entrar
def decoradorPermitirC(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth and (auth[2] == 1):
            return funcionPrincipal(request, *args, **kwargs)
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index') 
    return autenticar

#Solo un Administrador y Cliente pueden entrar
def decoradorPermitirAC(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth and (auth[2] == 1 or auth[2] == 3):
            return funcionPrincipal(request, *args, **kwargs)
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index') 
    return autenticar
#---------------------------------------------------------------- Decoradores ----------------------------------------------------------------

#-----------------------------------------------Validacion de url que requiere id pero no lo llevan----------------------------
def sinId(request):
    messages.error(request, f'No digitó una id')
    return redirect('paginaWeb:index')
#-----------------------------------------------Validacion de url que requiere id pero no lo llevan--------------------------

# Create your views here.
def index(request):
    return render(request, 'run/index.html')


#Login
@decoradorDenegarAEC
def loginForm(request):
    """Método para acceder al formulario de logueo"""
    return render(request, 'run/login/login.html')

@decoradorDenegarAEC
def login(request):
    """Autenticación y control de acceso 
    de los usuarios del sistema 
    """
    if request.method == 'POST':
        try:
            correo = request.POST['email']
            passw = request.POST['passw']

            q = Personas.objects.get(correo = correo, contrasena = passw)
            print(correo)

            request.session['auth'] = [q.correo,q.contrasena,q.roles.id_roles]

            messages.success(request, f'Bienvenid@ {q.correo}')
        except Exception as e:
            messages.error(request, f'Correo o contraseña incorrectos...')
            return redirect('paginaWeb:login_form')
    else:
        messages.warning(request, '¿Qué estás haciendo?')
    
    return redirect('paginaWeb:index')

@decoradorPermitirAEC
def logout(request):
    """Cerrar session actual, elimina cookie de sesion para ello 
    """
    try:
        del request.session['auth']
        messages.success(request, 'Sesión cerrada correctamente')
    except Exception as e:
        messages.error(request, f"Ocurrió un error, intente de nuevo...")
    
    return redirect('paginaWeb:index')


#Personas 
def perfil(request):
    """retorna acceso al perfil del usuario
    """
    auth = request.session.get('auth', False)
    q = Personas.objects.get(correo = auth[0])

    contexto = {'usuario': q}

    return render(request, 'run/perfil/perfil.html', contexto)

@decoradorDenegarAEC
def registro(request):
    """Autenticación y control de acceso 
    de los usuarios del sistema 
    """
    return render(request, 'run/registros/registro.html')

@decoradorDenegarAEC
def guardarPersona(request):
    """Autentica y guarda nuevo registro de usuario(Persona) en el sistema 
    """
    if request.method == 'POST':
        try:    
            CoExistente = Personas.objects.filter(correo=request.POST['Correo'])
            ceduExistente = Personas.objects.filter(cedula= request.POST['Id'])
            if CoExistente:
                messages.error(request, "Correo ya registrado, ingrese uno diferente por favor")
                return render(request, 'run/registros/registro.html')
            elif ceduExistente:
                messages.error(request, "cedula ya registrada, ingrese una diferente por favor")
                return render(request, 'run/registros/registro.html')
            else:
                if request.FILES:
                    #crear instancia de File System Storage
                    fss = FileSystemStorage()
                    #capturar la foto del formulario
                    f = request.FILES["imagen"]
                    #cargar archivos al servidor
                    file = fss.save("RUN/fotoUsuario/"+f.name, f)
                else:
                    file = "RUN/fotoUsuario/default.png"

                usuarioNew = Personas(
                    cedula = request.POST['Id'],
                    foto = file,
                    nombre = request.POST['Nombre'],
                    apellido = request.POST['Apellidos'],
                    celular = request.POST['Celular'],
                    fecha_nacimiento = request.POST['FechaNacim'],
                    direccion = request.POST['Direccion'],
                    tipo = "No lo sé", #No sé qué se coloca aqui
                    correo = request.POST['Correo'],
                    contrasena = request.POST['contrasena'], 
                    roles = Roles.objects.get(pk=1)
                )
                usuarioNew.save()
                #return render(request, 'run/login/login.html')
                messages.success(request, "Usuario registrado exitosamente")
                return redirect('paginaWeb:list_usu')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return render(request, 'run/registros/registro.html')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return render(request, 'run/index.html')

#Registros clientes



@decoradorPermitirAC
def eliminarPersona(request, id):
    """Elimina un usuario(Persona)
    """
    try:
        usuario = Personas.objects.get(cedula=id)
        from pathlib import Path
        from os import remove, path 
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent


        ruta_imagen =  str(BASE_DIR)+str(usuario.foto.url)

        #buscamos si existe la ruta
        if path.exists(ruta_imagen):
            #si es diferente a la default la borramos, ya que no podemos borrar la imagen por predeterminado
            print(usuario.foto.url)
            if usuario.foto.url != "/uploads/RUN/fotoUsuario/default.png":
                remove(ruta_imagen)
                messages.success(request,"Foto borrada correctamente.")
            else:
                print("La foto del usuario es predeterminada")
            #     messages.warning(request,"No se puede borrar la foto debido a que es la que tiene por pre--determinado.")
        usuario.delete()
        messages.success(request, "Eliminado correctamente")
        return redirect ('paginaWeb:list_usu')
    except Exception as e:
        messages.error(request, f"Hubo un error al eliminar el usuario : {e}")
        return redirect ('paginaWeb:list_usu')
    
@decoradorPermitirC
def updatePersona(request):
    """Actualiza la información de un usuario(Persona)
    """
    if request.method == "POST":
        try:
            persona = Personas.objects.get(pk=request.POST['cedula'])

            if request.POST['password'] != "":
                persona.contrasena = (request.POST['password'])#claveEncriptada

            if request.FILES:
                #crear instancia de File System Storage
                fss = FileSystemStorage()
                #capturar la foto del formulario
                f = request.FILES["foto"]
                #cargar archivos al servidor
                file = fss.save("RUN/fotoUsuario/"+f.name, f)

                #Mi manera de borrar
                import os 
                from django.conf import settings
                #base = str()
                #Borrar imagen anterior
                if persona.foto.url != "RUN/fotoUsuario/default.png":
                    fotoVieja = str(settings.BASE_DIR)+persona.foto.url
                    os.remove(fotoVieja)
                    messages.success(request,"Foto borrada correctamente.")
                
                #print(f"{settings.BASE_DIR}/{a.foto.url[1:]}")
                #asignamos la foto
                persona.foto = file

            persona.nombre = request.POST['nombre']
            persona.apellido = request.POST['apellidos']
            persona.celular = request.POST['telefono']
            persona.direccion = request.POST['direccion']
            #persona.roles = Roles.objects.get(pk=request.POST['rol'])
            persona.save()
            messages.success(request, "Actualizado correctamente")
            return redirect('paginaWeb:list_usu')
        except Exception as e:
            messages.error(request, f"Hubo un error al momento de actualizar: {e}")
            return redirect('paginaWeb:list_usu')

    else:
        messages.warning(request, "No sabemos por donde se esta metiendo pero no puedes avanzar, puerco")
        return redirect('paginaWeb:list_usu')

#hubo problemas con el nombre, luego se cambian
@decoradorPermitirAE
def listarPersonas(request):
    """Trae todos los usuarios activos en el momento para mostrarlos en un html
    """
    q = Personas.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/personas/listarPersonas.html', contexto)

@decoradorPermitirAEC
def buscarPersonaEditar(request, id):
    """No lo sé
    """
    q = Personas.objects.get(pk = id)

    contexto = {'personas': q}

    return render(request, 'run/personas/editarPersonas.html', contexto)


#Marcas
@decoradorPermitirAE
def formMarcas(request):
    return render(request, 'run/marcas/marcasForm.html')

@decoradorPermitirAEC
def listarMarcas(request):

    q = Marcas.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/marcas/listarMarcas.html', contexto)

@decoradorPermitirAE
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

@decoradorPermitirAE
def deleteMarcas(request, id):
    try:
        marca = Marcas.objects.get(pk = id)
        marca.delete()
        messages.success(request, 'Marca eliminada correctamente')
        return redirect('paginaWeb:list_marcas')
    except Exception as e: 
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'La marca esta vinculada a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_marcas')
        else:
            messages.error(request, f'Hubo un problema al eliminar una marca: {e}')
            return redirect('paginaWeb:list_marcas')


@decoradorPermitirAE
def updateMarcasForm(request, id):

    q = Marcas.objects.get(pk = id)

    contexto = {'marcas': q}

    return render(request, 'run/marcas/editarMarcas.html', contexto)

@decoradorPermitirAE
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
    """Método para visualizar los productos ofrecidos en la tienda"""

    q = Productos.objects.all()

    producto = q
    s = Imagenes.objects.filter(productos = producto)
    i = Imagenes.objects.all()

    contexto = {'productos': q, 'imagenes':i}

    return render(request, 'run/compras/compras.html', contexto)


#Imagenes
def regImagenesForm(request):
    """Formulario para acceder al registro
    de imagenes nuevas para los productos
    """
    p = Productos.objects.all()
    contexto = {'productos':p}
    return render(request, 'run/imagenes/registrar_imagenes.html', contexto)


def regImagenes(request):
    """Método para guardar las imagenes 
    con su respectivo producto
    """
    if request.method == "POST":
        try:
            if request.FILES:
                #crear instancia de File System Storage
                fss = FileSystemStorage()
                #capturar la foto del formulario
                f = request.FILES["imagen"]
                #cargar archivos al servidor
                file = fss.save("RUN/imagProductos/"+f.name, f) #    Guardar en esta ruta, esta imagen.
            else:
                file = "RUN/imagProductos/default.png"
            
            q = Imagenes(
                id_imagen = request.POST['idImagen'],
                imagen = file,
                productos = Productos.objects.get(pk = request.POST['producto']),
            ) 
            q.save()
            messages.success(request, "Imagen guardadada correctamente!!!")
        except Exception as e:
            messages.error(request, f"Ha ocurrido un error {e}")
            return redirect('paginaWeb:reg_imagenes_form')
    else:
        messages.warning(request, "Estás haciendo cosas raras...")
    
    return redirect('paginaWeb:list_imagenes')

def listImagenes(request):
    """Método para listar las imagenes"""
    q = Imagenes.objects.all()
    contexto = {'imagenes': q}
    return render(request, 'run/imagenes/listar_imagenes.html', contexto)
    

#Inventario
@decoradorPermitirAE
def registroInventario(request):
    q = Marcas.objects.all()

    contexto = {'dataMarcas': q}
    #print(contexto)

    return render(request, 'run/registros/registroInventario.html', contexto)

@decoradorPermitirAE
def listarInventario(request):

    q = Productos.objects.all()

    contexto = {'productos': q}

    return render(request, 'run/inventario/listarInventario.html', contexto)

@decoradorPermitirAE
def crearInventario(request): 
    try:
        if request.FILES:
            #crear instancia de File System Storage
            fss = FileSystemStorage()
            #capturar la foto del formulario
            f = request.FILES["imagen"]
            #cargar archivos al servidor
            file = fss.save("RUN/imagProductos/"+f.name, f)
        else:
            file = "RUN/imagProductos/default.png"
        
        q = Productos(
            id_producto = request.POST['codigo'],
            nombre_producto = request.POST['nombreRes'],
            stock = request.POST['stock'],
            precio = request.POST['precio'],
            marca = Marcas.objects.get(pk = request.POST['marca']),
            descripcion = request.POST['descripcion'],
            imagen = file
        ) 
        q.save()
        return redirect('paginaWeb:list_inv')
        
    except Exception as e:
        messages.error(request, f'Hubo un problema al intentar agregar : {e}')
        return redirect('paginaWeb:list_inv')

@decoradorPermitirAE
def deleteInventario(request, id):
    try:
        producto = Productos.objects.get(pk=id)
        from pathlib import Path
        from os import remove, path 
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent


        ruta_imagen =  str(BASE_DIR)+str(producto.imagen.url)

        #buscamos si existe la ruta
        if path.exists(ruta_imagen):
            #si es diferente a la default la borramos, ya que no podemos borrar la imagen por predeterminado
            
            print("Este es el nuevo url")
            
            print(producto.imagen.url)
            if producto.imagen.url != "/uploads/RUN/imagProductos/default.png":
                remove(ruta_imagen)
                messages.success(request,"Foto borrada correctamente.")
            else:
                messages.warning(request,"No se puede borrar la foto debido a que es la que tiene por pre--determinado.")

        producto.delete()
        messages.success(request, 'Producto eliminado correctamente')
        return redirect('paginaWeb:list_inv')
    except Exception as e:
        messages.error(request, f'Hubo un problema al intentareliminar : {e}')
        return redirect('paginaWeb:list_inv')

@decoradorPermitirAE
def updateInventarioForm(request, id):

    q = Productos.objects.get(pk=id)
    m = Marcas.objects.all()

    contexto = {'productos': q, 'dataMarcas': m}
    
    return render(request, 'run/inventario/editarInventario.html', contexto)


@decoradorPermitirAE
def updateInventario(request):
    if request.method == "POST":
        try:
            productos = Productos.objects.get(pk = request.POST['codigo'])
            if request.FILES and request.FILES["imagen"]:
                
                #crear instancia de File System Storage
                fss = FileSystemStorage()
                #capturar la foto del formulario
                f = request.FILES["imagen"]
                #cargar archivos al servidor
                file = fss.save("RUN/imagProductos/"+f.name, f)
            
                #Mi manera de borrar
                import os 
                from django.conf import settings
                #Borrar imagen anterior
                if productos.imagen.url != "territorio/fotos/default.png":
                    fotoVieja = str(settings.BASE_DIR)+productos.imagen.url
                    os.remove(fotoVieja)
                    #messages.success(request,"Foto borrada correctamente.")

                #asignamos la foto
                productos.imagen = file


            productos.nombre_producto = request.POST['nombreRes']
            productos.stock = request.POST['stock']
            productos.precio = request.POST['precio']
            productos.marca = Marcas.objects.get(pk = request.POST['marca'])
            productos.descripcion = request.POST['descripcion']
            productos.save()
            messages.success(request, 'Producto correctamente editado')

        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al intenar editar: {e}')
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
@decoradorPermitirC
def carritoCompras(request):

    q = Productos.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/carritoCompras.html', contexto)

@decoradorPermitirC
def addCarrito(request, id):
    try:    
        q = Productos.objects.get(pk=id)
        listaCarrito = request.session.get('carrito', False)

        if listaCarrito: 
            
            listaCarrito.append(id)
            request.session['carrito'] = listaCarrito
        else:
            request.session['carrito'] = [id]


        messages.success(request, 'Producto agregado correctamente al carrito')
        return redirect('paginaWeb:ver_prod')
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error al agregara el producto al carrito, vuelvalo a intentar mas tarde {e}')
        return redirect('paginaWeb:ver_prod')

@decoradorPermitirC
def mostrarCarrito(request):
    try:    
        
        carrito = request.session.get('carrito', False)
        listaCarrito = []

        if carrito:
            print(carrito)
            for i in carrito:
                q =Productos.objects.get(pk=i)
                listaCarrito.append(q)

        contexto = {'productos': listaCarrito}   

        return render(request, 'run/carritoCompras.html', contexto)
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error al traer los productos del carrito, vuelvalo a intentar mas tarde {e}')
        return redirect('paginaWeb:ver_prod')

@decoradorPermitirC
def vaciarCarrito(request):
    try:
        if request.session.get('carrito', False):
            del request.session['carrito']

        messages.success(request, 'Borrado Existosamente')

        return redirect('paginaWeb:ver_prod')
    except Exception as e:
        messages.error(request, f'Ha ocurrido al borrar el carrito: {e}')
        return redirect('paginaWeb:ver_prod')

@decoradorPermitirC
def borrarElementoCarrito(request, id):
    try:
        if request.session.get('carrito', False):
            carrito = request.session.get('carrito', False)
            carrito.remove(id)
            request.session['carrito'] = carrito


        messages.success(request, 'Borrado Existosamente')

        return redirect('paginaWeb:carrito')
    except Exception as e:
        messages.error(request, f'Ha ocurrido al borrar el carrito: {e}')
        return redirect('paginaWeb:ver_prod')


#Admin - Roles
@decoradorPermitirAE
def listRoles(request):

    q = Roles.objects.all()

    contexto = {'roles': q}

    return render(request, 'run/listarRoles.html', contexto)

@decoradorPermitirA
def regRolesForm(request):
    return render(request, 'run/registros/registroRoles.html')

@decoradorPermitirA
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

@decoradorPermitirA
def deleteRol(request, id):
    try:
        rol = Roles.objects.get(pk=id)
        rol.delete()
        messages.success(request, 'Rol eliminado correctamente')
        return redirect('paginaWeb:list_roles')
    except Exception as e:
        messages.error(request, f'Hubo un error al intentar eliminar un rol: {e}')
        return redirect('paginaWeb:list_roles')

@decoradorPermitirA
def updateRolForm(request, id):

    q = Roles.objects.get(pk=id)

    contexto = {'roles':q}

    return render(request, 'run/roles/editarRoles.html', contexto)

@decoradorPermitirA
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
@decoradorPermitirA
def formUsuarios(request):
    return render(request, 'run/usuarios/usuariosForm.html')

@decoradorPermitirA
def listarUsuarios(request):

    q = Usuarios.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/usuarios/listarUsuarios.html', contexto)

@decoradorPermitirA
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

@decoradorPermitirA
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

@decoradorPermitirA
def updateUsuariosForm(request, id):

    q = Usuarios.objects.get(pk = id)

    contexto = {'usuarios': q}

    return render(request, 'run/usuarios/editarUsuarios.html', contexto)

@decoradorPermitirA
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
@decoradorPermitirA
def formEmpleados(request):
    return render(request, 'run/empleados/empleadosForm.html')

@decoradorPermitirA
def listarEmpleados(request):

    q = Empleados.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/empleados/listarEmpleados.html', contexto)

@decoradorPermitirA
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

@decoradorPermitirA
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

@decoradorPermitirA
def updateEmpleadosForm(request, id):

    q = Empleados.objects.get(pk = id)

    contexto = {'empleados': q}

    return render(request, 'run/empleados/editarEmpleados.html', contexto)

@decoradorPermitirA
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
@decoradorPermitirAE
def formVentas(request):

    e = Envios.objects.all()
    p = Pedidos.objects.all()

    contexto = {'envios': e, 'pedidos': p}


    return render(request, 'run/ventas/ventasForm.html', contexto)

@decoradorPermitirAE
def listarVentas(request):

    q = Ventas.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/ventas/listarVentas.html', contexto)

@decoradorPermitirAE
def addVentas(request):
    if request.method == 'POST':
        try:    
            ventaExistente = Ventas.objects.filter(id_venta=request.POST['id_venta'])
            # pedidoExistente = Pedidos.objects.filter(id_pedido=request.POST['pedido'])
            # envioExistente = Envios.objects.filter(id_envio= request.POST['envio'])
            if ventaExistente:
                messages.error(request, "id de Venta ya registrada, ingrese una diferente por favor")
                return redirect('paginaWeb:form_ventas')
            else:
                q = Ventas(
                    id_venta = request.POST['id_venta'],
                    pedido = Pedidos.objects.get(pk=request.POST['pedido']),
                    envio = Envios.objects.get(pk=request.POST['envio']))
                q.save()
                messages.success(request, "Venta registrada exitosamente")
                return redirect('paginaWeb:list_ventas')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:form_ventas')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return redirect('paginaWeb:list_ventas')

@decoradorPermitirAE
def deleteVentas(request, id):
    try:
        venta = Ventas.objects.get(pk = id)
        venta.delete()
        messages.success(request, 'Venta eliminada correctamente')
        return redirect('paginaWeb:list_ventas')
    except Exception as e: 
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'La venta esta vinculada a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_ventas')
        else:
            messages.error(request, f'Hubo un problema al eliminar una venta: {e}')
            return redirect('paginaWeb:list_ventas')

@decoradorPermitirAE
def updateVentasForm(request, id):

    q = Ventas.objects.get(pk = id)
    e = Envios.objects.all()
    p = Pedidos.objects.all()

    contexto = {'ventas': q, 'envios': e, 'pedidos': p}

    return render(request, 'run/ventas/editarVentas.html', contexto)

@decoradorPermitirAE
def updateVentas(request):
    
    if request.method == "POST":
        try:
            venta = Ventas.objects.get(id_venta=request.POST['id_venta'])
            pedidoExistente = Pedidos.objects.filter(id_pedido=request.POST['pedido'])
            envioExistente = Envios.objects.filter(id_envios= request.POST['envio'])
            if not pedidoExistente:
                messages.error(request, "id de pedido inexistente, ingrese uno que exista")
                return redirect('paginaWeb:upd_ventas_form')
            elif not envioExistente:
                messages.error(request, "id de producto inexistente, ingrese un que exista")
                return redirect('paginaWeb:upd_ventas_form')
            else:
                venta.pedido = Pedidos.objects.get(pk=request.POST['pedido'])
                venta.envio = Envios.objects.get(pk = request.POST['envio'])
                venta.save()
                #print(Productos.objects.get(pk = request.POST['producto']))
                messages.success(request, "Venta actualizada exitosamente")
                return redirect('paginaWeb:list_ventas')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:upd_ventas_form')

#Pedidos
@decoradorPermitirAE
def formPedidos(request):

    q = Clientes.objects.all()

    contexto = {'clientes': q}


    return render(request, 'run/pedidos/pedidosForm.html', contexto)

@decoradorPermitirAE
def listarPedidos(request):

    q = Pedidos.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/pedidos/listarPedidos.html', contexto)

@decoradorPermitirAE
def addPedidos(request):
    if request.method == 'POST':
        try:    
            CoExistente = Clientes.objects.filter(id=request.POST['cliente'])
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

@decoradorPermitirAE
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

@decoradorPermitirAE
def updatePedidosForm(request, id):

    q = Pedidos.objects.get(pk = id)
    c = Clientes.objects.all()
    contexto = {'pedidos': q, 'clientes': c}

    return render(request, 'run/pedidos/editarPedidos.html', contexto)


@decoradorPermitirAE
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

#PedidosProductos
@decoradorPermitirA
def formPedidosProductos(request):
    p = Pedidos.objects.all()

    pr = Productos.objects.all()

    contexto = {'pedidos': p, 'productos': pr}

    return render(request, 'run/pedidosProductos/pedidosProductosForm.html', contexto)

@decoradorPermitirA
def listarPedidosProductos(request):

    q = PedidosProductos.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/pedidosProductos/listarPedidosProductos.html', contexto)

@decoradorPermitirA
def addPedidosProductos(request):
    if request.method == 'POST':
        try:    
            pedidoProExistente = PedidosProductos.objects.filter(id_pedidos_productos=request.POST['id_pedidos_productos'])
            pedidoExistente = Pedidos.objects.filter(id_pedido=request.POST['pedido'])
            productoExistente = Productos.objects.filter(id_producto= request.POST['producto'])
            if pedidoProExistente:
                messages.error(request, "id de pedidoProducto ya existente, ingrese uno diferente")
                return redirect('paginaWeb:form_pedidos_productos')
            elif not pedidoExistente:
                messages.error(request, "id de pedido inexistente, ingrese uno que exista")
                return redirect('paginaWeb:form_pedidos_productos')
            elif not productoExistente:
                messages.error(request, "cedula ya registrada, ingrese una diferente por favor")
                return redirect('paginaWeb:form_pedidos_productos')
            else:
                q = PedidosProductos(
                    id_pedidos_productos = request.POST['id_pedidos_productos'],
                    pedido = Pedidos.objects.get(pk=request.POST['pedido']),
                    producto = Productos.objects.get(pk = request.POST['producto']))
                q.save()
                messages.success(request, "Empleado registrado exitosamente")
                return redirect('paginaWeb:list_pedidos_productos')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:form_pedidos_productos')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return redirect('paginaWeb:list_pedidos_productos')

@decoradorPermitirA
def deletePedidosProductos(request, id):
    try:
        pedidoProducto = PedidosProductos.objects.get(id_pedidos_productos = id)
        pedidoProducto.delete()
        messages.success(request, 'pedidoProducto eliminado correctamente')
        return redirect('paginaWeb:list_pedidos_productos')
    except Exception as e: 
        messages.error(request, f'Hubo un problema al eliminar un pedidoProducto: {e}')
        return redirect('paginaWeb:list_pedidos_productos')

@decoradorPermitirA
def updatePedidosProductosForm(request, id):

    pp = PedidosProductos.objects.get(pk = id)
    p = Pedidos.objects.all()

    pr = Productos.objects.all()

    contexto = {'pedidoProducto':pp, 'pedidos': p, 'productos': pr}

    return render(request, 'run/pedidosProductos/editarPedidosProductos.html', contexto)

@decoradorPermitirA
def updatePedidosProductos(request):
    
    if request.method == "POST":
        try:
            pedidoProducto = PedidosProductos.objects.get(id_pedidos_productos=request.POST['id_pedidos_productos'])
            pedidoExistente = Pedidos.objects.filter(id_pedido=request.POST['pedido'])
            productoExistente = Productos.objects.filter(id_producto= request.POST['producto'])
            if not pedidoExistente:
                messages.error(request, "id de pedido inexistente, ingrese uno que exista")
                return redirect('paginaWeb:upd_pedidos_productos_form')
            elif not productoExistente:
                messages.error(request, "id de producto inexistente, ingrese un que exista")
                return redirect('paginaWeb:upd_pedidos_productos_form')
            else:
                print(pedidoProducto.pedido, pedidoProducto.producto)
                pedidoProducto.pedido = Pedidos.objects.get(pk=request.POST['pedido'])
                pedidoProducto.producto = Productos.objects.get(pk = request.POST['producto'])
                pedidoProducto.save()
                #print(Productos.objects.get(pk = request.POST['producto']))
                messages.success(request, "pedidoProducto registrado exitosamente")
                return redirect('paginaWeb:list_pedidos_productos')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:upd_pedidos_productos_form')

#Envios
@decoradorPermitirAE
def listEnvios(request):

    q = Envios.objects.all()

    contexto = {'envios': q}

    return render(request, 'run/envios/listarEnvios.html', contexto)

@decoradorPermitirAE
def formEnvios(request):
    return render(request, 'run/envios/enviosForm.html')

@decoradorPermitirAE
def addEnvios(request):
    if request.method == 'POST':
        try:    
            q = Envios(
                id_envios = request.POST['idEnvio'],
                fecha_envio = request.POST['fecha'],
                direccion_envio = request.POST['dir'],
            )
            q.save()
            messages.success(request, "Envio registrado exitosamente")
            return redirect('paginaWeb:list_envios')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:form_envios')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return redirect('paginaWeb:list_envios')

@decoradorPermitirAE
def deleteEnvios(request, id):
    try:
        envio = Envios.objects.get(pk= id)
        envio.delete()
        messages.success(request, 'Envio eliminado correctamente')
        return redirect('paginaWeb:list_envios')
    except Exception as e: 
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'El Envio esta vinculado a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_envios')
        else:
            messages.error(request, f'Hubo un problema al eliminar un Envio: {e}')
            return redirect('paginaWeb:list_envios')

@decoradorPermitirAE
def updateEnviosForm(request, id):

    q = Envios.objects.get(pk = id)
    contexto = {'envios': q}
    return render(request, 'run/envios/editarEnvio.html', contexto)

@decoradorPermitirAE
def updateEnvios(request):
    
    if request.method == "POST":
        try: 
            envio = Envios.objects.get(id_envios=request.POST['idEnvio'])

            envio.fecha_envio = request.POST['fecha']
            envio.direccion_envio = request.POST['dir']
            envio.save()

            messages.success(request, "Actualizado correctamente")
            return redirect('paginaWeb:list_envios')
        except Exception as e:
            messages.error(request, f"Hubo un error al momento de actualizar: {e}")
            return redirect('paginaWeb:list_envios')
    else:
        messages.warning(request, "No sabemos por donde se esta metiendo pero no puedes avanzar, puerco")
        return redirect('paginaWeb:list_envios')


#MediosDePago
@decoradorPermitirA
def listMediosPagos(request):

    q = MediosDePagos.objects.all()

    contexto = {'medios': q}

    return render(request, 'run/mediosPagos/listarMediosPagos.html', contexto)

@decoradorPermitirA
def formMediosPagos(request):
    return render(request, 'run/mediosPagos/mediosPagosForm.html')

@decoradorPermitirA
def addMediosPagos(request):
    if request.method == 'POST':
        try:    
            q = MediosDePagos(
                id_medio_pago = request.POST['idMedio'],
                nombre_medio_pago = request.POST['nombreMedio'],
                estado_medio_pago = request.POST['estado'],
            )
            q.save()
            messages.success(request, "Medio de pago registrado exitosamente")
            return redirect('paginaWeb:list_mediosPagos')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:form_mediosPagos')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return redirect('paginaWeb:list_mediosPagos')

@decoradorPermitirA
def deleteMediosPagos(request, id):
    try:
        medioPago = MediosDePagos.objects.get(pk= id)
        medioPago.delete()
        messages.success(request, 'Medio de pago eliminado correctamente')
        return redirect('paginaWeb:list_mediosPagos')
    except Exception as e: 
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'El medio de pago está vinculado a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_mediosPagos')
        else:
            messages.error(request, f'Hubo un problema al eliminar un medio de pago: {e}')
            return redirect('paginaWeb:list_mediosPagos')

@decoradorPermitirA
def updateMediosPagosForm(request, id):

    q = MediosDePagos.objects.get(pk = id)
    a = MediosDePagos.objects.all()
    contexto = {'medios': q, 'medPagos': a}
    return render(request, 'run/mediosPagos/editarMedioPago.html', contexto)

@decoradorPermitirA
def updateMediosPagos(request):
    
    if request.method == "POST":
        try: 
            medioPago = MediosDePagos.objects.get(id_medio_pago=request.POST['idMedio'])

            medioPago.nombre_medio_pago = request.POST['nombreMedio']
            medioPago.estado_medio_pago = request.POST['estado']
            medioPago.save()

            messages.success(request, "Actualizado correctamente")
            return redirect('paginaWeb:list_mediosPagos')
        except Exception as e:
            messages.error(request, f"Hubo un error al momento de actualizar: {e}")
            return redirect('paginaWeb:list_mediosPagos')
    else:
        messages.warning(request, "No sabemos por donde se está metiendo pero no puedes avanzar, puerco")
        return redirect('paginaWeb:list_mediosPagos')


#Pagos
@decoradorPermitirAE
def listPagos(request):

    q = Pagos.objects.all()

    contexto = {'pagos': q}

    return render(request, 'run/pagos/listarPagos.html', contexto)

@decoradorPermitirA
def formPagos(request):

    q = MediosDePagos.objects.all()

    contexto = {'medPagos': q}
    return render(request, 'run/pagos/pagosForm.html', contexto)

@decoradorPermitirA
def addPagos(request):
    if request.method == 'POST':
        try:    
            q = Pagos(
                id_pago = request.POST['idPago'],
                medio_pago = MediosDePagos.objects.get(pk = request.POST['medioPago']),
                fecha_pagos = request.POST['fecha'],
            )
            q.save()
            messages.success(request, "Pago registrado exitosamente")
            return redirect('paginaWeb:list_pagos')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:form_pagos')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return redirect('paginaWeb:list_pagos')

@decoradorPermitirA
def deletePagos(request, id):
    try:
        pagos = Pagos.objects.get(pk= id)
        pagos.delete()
        messages.success(request, 'Pago eliminado correctamente')
        return redirect('paginaWeb:list_pagos')
    except Exception as e: 
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'El pago está vinculado a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_pagos')
        else:
            messages.error(request, f'Hubo un problema al eliminar un pago: {e}')
            return redirect('paginaWeb:list_pagos')

@decoradorPermitirA
def updatePagosForm(request, id):

    q = Pagos.objects.get(pk = id)
    a = MediosDePagos.objects.all()
    contexto = {'pagos': q, 'medPagos': a}
    return render(request, 'run/pagos/editarPagos.html', contexto)

@decoradorPermitirA
def updatePagos(request):
    
    if request.method == "POST":
        try: 
            pagos = Pagos.objects.get(id_pago=request.POST['idPago'])

            pagos.medio_pago = MediosDePagos.objects.get(pk = request.POST['medioPago'])
            pagos.fecha_pagos = request.POST['fecha']
            pagos.save()

            messages.success(request, "Actualizado correctamente")
            return redirect('paginaWeb:list_pagos')
        except Exception as e:
            messages.error(request, f"Hubo un error al momento de actualizar: {e}")
            return redirect('paginaWeb:list_pagos')
    else:
        messages.warning(request, "No sabemos por donde se está metiendo pero no puedes avanzar, puerco")
        return redirect('paginaWeb:list_pagos') 

#Historial
@decoradorPermitirA
def formHistorial(request):

    v = Ventas.objects.all()
    p = Pagos.objects.all()

    contexto = {'ventas': v, 'pagos': p}


    return render(request, 'run/historial/historialForm.html', contexto)

@decoradorPermitirAE
def listarHistorial(request):

    q = Historial.objects.all()

    contexto = {'datos': q}

    return render(request, 'run/historial/listarHistorial.html', contexto)

@decoradorPermitirA
def addHistorial(request):
    if request.method == 'POST':
        try:    
            historialExistente = Historial.objects.filter(id_historial=request.POST['id_historial'])
            if historialExistente:
                messages.error(request, "id de Historial ya registrada, ingrese una diferente por favor")
                return redirect('paginaWeb:form_historial')
            else:
                q = Historial(
                    id_historial = request.POST['id_historial'],
                    venta = Ventas.objects.get(pk=request.POST['venta']),
                    pago = Pagos.objects.get(pk=request.POST['pago']))
                q.save()
                messages.success(request, "Registro de historial registrado exitosamente")
                return redirect('paginaWeb:list_historial')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:form_historial')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return redirect('paginaWeb:list_historial')

@decoradorPermitirA
def deleteHistorial(request, id):
    try:
        historial = Historial.objects.get(pk = id)
        historial.delete()
        messages.success(request, 'Registro de historial eliminado correctamente')
        return redirect('paginaWeb:list_historial')
    except Exception as e: 
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'El historial esta vinculadao a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_historial')
        else:
            messages.error(request, f'Hubo un problema al eliminar un historial: {e}')
            return redirect('paginaWeb:list_historial')

@decoradorPermitirA
def updateHistorialForm(request, id):

    h = Historial.objects.get(pk = id)
    v = Ventas.objects.all()
    p = Pagos.objects.all()

    contexto = {'historial': h, 'ventas': v, 'pagos': p}

    return render(request, 'run/historial/editarHistorial.html', contexto)

@decoradorPermitirA
def updateHistorial(request):
    
    if request.method == "POST":
        try:
            historial = Historial.objects.get(id_historial=request.POST['id_historial'])
            ventaExistente = Ventas.objects.filter(id_venta=request.POST['venta'])
            pagoExistente = Pagos.objects.filter(id_pago= request.POST['pago'])
            if not ventaExistente:
                messages.error(request, "id de pedido inexistente, ingrese uno que exista")
                return redirect('paginaWeb:upd_historial_form')
            elif not pagoExistente:
                messages.error(request, "id de producto inexistente, ingrese un que exista")
                return redirect('paginaWeb:upd_historial_form')
            else:
                historial.Venta = Ventas.objects.get(pk=request.POST['venta'])
                historial.pago = Pagos.objects.get(pk = request.POST['pago'])
                historial.save()
                #print(Productos.objects.get(pk = request.POST['producto']))
                messages.success(request, "Historial actualizado exitosamente")
                return redirect('paginaWeb:list_historial')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:upd_historial_form')
