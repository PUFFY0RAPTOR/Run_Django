from email import message
from urllib import request
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from .cryp import claveEncriptada

# almacenamiento de archivos o fotos
from django.core.files.storage import FileSystemStorage


# ---------------------------------------------------------------- Decoradores ----------------------------------------

# A = Administrador, E = Empleado, C = CLiente

# Decorador para controlar la entrada desde las rutas
def decoradorPermitirAE(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth and (auth[2] == 3 or auth[2] == 2):
            return funcionPrincipal(request, *args, **kwargs)
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')

    return autenticar


# NO puede entrar los administradores ni tampoco los empleados ni los clientes, nadie logueado
def decoradorDenegarAEC(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')
        else:
            return funcionPrincipal(request, *args, **kwargs)  # Ahorrar codigo explicar a sebas

    return autenticar


# No puede entrar a menos que este logueado
def decoradorPermitirAEC(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth:
            return funcionPrincipal(request, *args, **kwargs)  # Ahorrar codigo explicar a sebas
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')

    return autenticar


# Solo un administrador puede entrar
def decoradorPermitirA(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth and (auth[2] == 3):
            return funcionPrincipal(request, *args, **kwargs)
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')

    return autenticar


# Solo un administrador y alguien que no este logueado, puede entrar
def decoradorPermitirAV(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth and (auth[2] == 3):
            return funcionPrincipal(request, *args, **kwargs)
        elif not auth:
            return funcionPrincipal(request, *args, **kwargs)
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')

    return autenticar


# Solo un Cliente puede entrar
def decoradorPermitirC(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth and (auth[2] == 1):
            return funcionPrincipal(request, *args, **kwargs)
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')

    return autenticar


# Solo un Administrador y Cliente pueden entrar
def decoradorPermitirAC(funcionPrincipal):
    def autenticar(request, *args, **kwargs):
        auth = request.session.get('auth', False)
        if auth and (auth[2] == 1 or auth[2] == 3):
            return funcionPrincipal(request, *args, **kwargs)
        else:
            messages.warning(request, 'No está autorizado para entrar a esta sección...')
            return redirect('paginaWeb:index')

    return autenticar


# ---------------------------------------------------------------- Decoradores --------------------------------------

# -----------------------------------------------Validacion de url que requiere id pero no lo llevan------------------
def sinId(request):
    messages.error(request, f'No digitó una id')
    return redirect('paginaWeb:index')


# -----------------------------------------------Validacion de url que requiere id pero no lo llevan--------------------

# Create your views here.
def index(request):
    """Método para ir a la página de inicio
    """
    return render(request, 'run/index.html')


# Login
@decoradorDenegarAEC
def loginForm(request):
    """Método para acceder al formulario de logueo
    """
    return render(request, 'run/login/login.html')


@decoradorDenegarAEC
def login(request):
    """Autenticación y control de acceso 
    de los usuarios del sistema 
    """
    if request.method == 'POST':
        try:
            correo = request.POST['email']
            passw = claveEncriptada(request.POST['passw'])
            q = Personas.objects.get(correo=correo, contrasena=passw)
            print(q)

            request.session['auth'] = [q.correo, q.contrasena, q.roles.id_roles]

            messages.success(request, f'Bienvenid@ {q.nombre}')
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


@decoradorDenegarAEC
def recuperarContraForm(request):
    """Método para acceder al formulario de recuperar contraseña
    """
    return render(request, 'run/login/recuperarContraForm.html')


@decoradorDenegarAEC
def enviarCorreo(request):
    """Método para enviar correo de recuperación
    """
    if request.method == "POST":
        try:
            variable = "Hola"
            persona = Personas.objects.get(correo=request.POST['correo'])
            from django.core.mail import send_mail
            try:
                cuerpoCorreo = 'Correo Para recuperar contraseña:/n http://127.0.0.1:8000/run/changePassForm/'+(claveEncriptada(str(persona.cedula)))+" si usted no solicitó este cambio entonces debería cambiar su contraseña," + \
                               "en RUN siempre queremos lo mejor para nuestros usuarios, hasta una proxima"
                send_mail(
                    'Correo de Recuperación de contraseña',
                    cuerpoCorreo,
                    'mateoortiz202@gmail.com',
                    ['mateo.ortiz54@misena.edu.co', request.POST['correo']],
                    fail_silently=False,
                )
                messages.success(request, "Correo enviado!")
                print("Correo Enviado")
                return redirect('paginaWeb:index')
            except Exception as e:
                messages.error(request, "Error!: " + str(e))
                print(e)
                return redirect('paginaWeb:index')
        except Exception as e:
            print(f"Persona con ese correo no existe{e}")
            return redirect('paginaWeb:index')
    else:
        messages.warning(request, 'Estás intentado hackear al ganador del SENASOFT? En serio?')
        return redirect('paginaWeb:index')


def changePassForm(request, id):
    personas = Personas.objects.all()
    for i in personas:
        if claveEncriptada(str(i.cedula)) == id:
            contexto = {'persona': i}
            messages.success(request, "Se encontró la id")
            return render(request, 'run/login/changePassword.html', contexto)
    messages.error(request, "No encontró la id")
    return redirect('paginaWeb:index')

@decoradorDenegarAEC
def savePassword(request):
    if request.method == "POST":
        try:
            persona = Personas.objects.get(pk=request.POST['cedula'])
            persona.contrasena = claveEncriptada(request.POST['contrasena'])
            persona.save()
            return redirect('paginaWeb:login_form')
        except Exception as e:
            messages.error(request, f'Hubo un error {e}')
            return redirect('paginaWeb:index')
    else:
        messages.warning(request, 'Estás intentado hackear al ganador del SENASOFT? En serio?')
        return redirect('paginaWeb:index')
# Personas
def perfil(request):
    """retorna acceso al perfil del usuario
    """
    auth = request.session.get('auth', False)
    q = Personas.objects.get(correo=auth[0])

    contexto = {'usuario': q}

    return render(request, 'run/personas/perfil.html', contexto)


decoradorPermitirAV
def registro(request):
    """Autenticación y control de acceso 
    de los usuarios del sistema 
    """
    q = Roles.objects.all()
    contexto = {'roles': q}
    return render(request, 'run/personas/registro.html', contexto)


@decoradorPermitirAEC
def guardarPersona(request):
    """Autentica y guarda nuevo registro de usuario(Persona) en el sistema
    """
    if request.method == 'POST':
        try:
            CoExistente = Personas.objects.filter(correo=request.POST['Correo'])
            ceduExistente = Personas.objects.filter(cedula=request.POST['Id'])
            if CoExistente:
                messages.error(request, "Correo ya registrado, ingrese uno diferente por favor")
                return render(request, 'run/personas/registro.html')
            elif ceduExistente:
                messages.error(request, "cedula ya registrada, ingrese una diferente por favor")
                return render(request, 'run/personas/registro.html')
            else:
                if request.FILES:
                    # crear instancia de File System Storage
                    fss = FileSystemStorage()
                    # capturar la foto del formulario
                    f = request.FILES["imagen"]
                    print(f"Esta es la F --- {f}")
                    # cargar archivos al servidor
                    file = fss.save("RUN/fotoUsuario/" + f.name, f)
                    print(f"Esta es el primer file: {file}")
                else:
                    file = "RUN/fotoUsuario/default.png"
                print(f"Este es el segundo: {file}")
                usuarioNew = Personas(
                    cedula=request.POST['Id'],
                    foto=file,
                    nombre=request.POST['Nombre'],
                    apellido=request.POST['Apellidos'],
                    celular=request.POST['Celular'],
                    fecha_nacimiento=request.POST['FechaNacim'],
                    direccion=request.POST['Direccion'],
                    correo=request.POST['Correo'],
                    contrasena=claveEncriptada(request.POST['contrasena']),
                    roles=Roles.objects.get(pk=1)
                )
                usuarioNew.save()
                # return render(request, 'run/login/login.html')
                messages.success(request, "Usuario registrado exitosamente")
                return redirect('paginaWeb:list_usu')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return render(request, 'run/personas/registro.html')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return render(request, 'run/index.html')


@decoradorPermitirAC
def eliminarPersona(request, id):
    """Elimina un usuario(Persona)
    """
    try:
        usuario = Personas.objects.get(pk=id)
        from pathlib import Path
        from os import remove, path
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent

        ruta_imagen = str(BASE_DIR) + str(usuario.foto.url)

        # buscamos si existe la ruta
        if path.exists(ruta_imagen):
            # si es diferente a la default la borramos, ya que no podemos borrar la imagen por predeterminado
            print(usuario.foto.url)
            if usuario.foto.url != "/uploads/RUN/fotoUsuario/default.png":
                remove(ruta_imagen)
                messages.success(request, "Foto borrada correctamente.")
            else:
                print("La foto del usuario es predeterminada")
            # messages.warning(request,"No se puede borrar la foto debido a que es la que tiene por pre--determinado.")
        usuario.delete()
        messages.success(request, "Eliminado correctamente")
        return redirect('paginaWeb:list_usu')
    except Exception as e:
        messages.error(request, f"Hubo un error al eliminar el usuario : {e}")
        return redirect('paginaWeb:list_usu')


@decoradorPermitirAEC
def updatePersona(request):
    """Actualiza la información de un usuario(Persona)
    """
    if request.method == "POST":
        try:
            persona = Personas.objects.get(pk=request.POST['cedula'])
            if request.POST['password'] and request.POST['password'] != "":
                persona.contrasena = claveEncriptada(request.POST['password'])
            if request.FILES:
                # crear instancia de File System Storage
                fss = FileSystemStorage()
                # capturar la foto del formulario
                f = request.FILES["foto"]
                # cargar archivos al servidor
                file = fss.save("RUN/fotoUsuario/" + f.name, f)

                # Mi manera de borrar
                import os
                from django.conf import settings
                # base = str()
                # Borrar imagen anterior
                if persona.foto.url != "RUN/fotoUsuario/default.png":
                    fotoVieja = str(settings.BASE_DIR) + persona.foto.url
                    os.remove(fotoVieja)
                    messages.success(request, "Foto borrada correctamente.")

                # print(f"{settings.BASE_DIR}/{a.foto.url[1:]}")
                # asignamos la foto
                persona.foto = file

            persona.nombre = request.POST['nombre']
            persona.apellido = request.POST['apellidos']
            persona.celular = request.POST['celular']
            persona.direccion = request.POST['direccion']
            #if request.POST['rol'] != "no aplica":
            #    persona.roles = Roles.objects.get(pk=request.POST['rol'])
            #if request.POST['fecha'] :
            #    persona.fecha = request.POST['fecha']
            # La fecha no aactualiza, se puede arreglar, creo
            persona.save()
            messages.success(request, "Actualizado correctamente")
            return redirect('paginaWeb:index')
            #return redirect('paginaWeb:list_usu')
        except UserWarning as e:
            messages.error(request, f"Hubo un error al momento de actualizar: {e}")
            return redirect('paginaWeb:list_usu')

    else:
        messages.warning(request, "No sabemos por donde se esta metiendo pero no puedes avanzar, puerco")
        return redirect('paginaWeb:list_usu')


# hubo problemas con el nombre, luego se cambian
@decoradorPermitirAE
def listarPersonas(request):
    """Trae todos los usuarios activos en
    el momento para mostrarlos en un html.
    """
    q = Personas.objects.all()

    contexto = {'personas': q}

    return render(request, 'run/personas/listarPersonas.html', contexto)


@decoradorPermitirAEC
def buscarPersonaEditar(request, id):
    """Método para encontrar una persona 
    para editarla.
    """
    q = Personas.objects.get(pk=id)
    r = Roles.objects.all()
    contexto = {'persona': q, 'roles': r}

    return render(request, 'run/personas/editarPersonas.html', contexto)


# Marcas
def marcas(request):
    """Método para acceder a visualizar
    las marcas.
    """
    return render(request, 'run/marcas/marcas.html')


@decoradorPermitirAE
def formMarcas(request):
    """Método para acceder al formulario
    de registro de marcas.
    """
    return render(request, 'run/marcas/marcasForm.html')


@decoradorPermitirAEC
def listarMarcas(request):
    """Método para acceder al formulario
        de registro de marcas.
    """
    q = Marcas.objects.all()
    contexto = {'datos': q}
    return render(request, 'run/marcas/listarMarcas.html', contexto)


@decoradorPermitirAE
def addMarcas(request):
    """Método para añadir marcas.
    """
    try:
        if request.FILES:
            fss = FileSystemStorage()
            f = request.FILES["imagen"]
            file = fss.save("RUN/fotoMarcas/" + f.name, f)
        else:
            file = "RUN/fotoMarcas/default.png"
        q = Marcas(
            id_marca=request.POST['id'],
            nombre_marca=request.POST['nombre'],
            imagen=file
        )
        q.save()
        messages.success(request, "Imagen guardada Correctamente")
        return redirect('paginaWeb:list_marcas')
    except Exception as e:
        messages.warning(request, "Hubo un error guardando la marca")
        return redirect('paginaWeb:list_marcas')


@decoradorPermitirAE
def deleteMarcas(request, id):
    """Método para eliminar marcas.
    """
    try:
        validation = Productos.objects.filter(marca=id)
        if validation:
            messages.warning(request, f'Marca asociada a otros registros, borralos y luego intentarlo de nuevo')
            return redirect('paginaWeb:list_marcas')

        marca = Marcas.objects.get(pk=id)
        from pathlib import Path
        from os import remove, path
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent

        ruta_imagen = str(BASE_DIR) + str(marca.imagen.url)

        # buscamos si existe la ruta
        if path.exists(ruta_imagen):
            # si es diferente a la default la borramos, ya que no podemos borrar la imagen por predeterminado
            print(marca.imagen.url)
            if marca.imagen.url != "/uploads/RUN/fotoMarcas/default.png":
                remove(ruta_imagen)
                messages.success(request, "Foto borrada correctamente.")
            else:
                print("La imagen de la marca es predeterminada")
        marca.delete()
        messages.success(request, 'Marca eliminada correctamente')
        return redirect('paginaWeb:list_marcas')
    except Exception as e:
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request,
                           f'La marca esta vinculada a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_marcas')
        else:
            messages.error(request, f'Hubo un problema al eliminar una marca: {e}')
            return redirect('paginaWeb:list_marcas')


@decoradorPermitirAE
def updateMarcasForm(request, id):
    """Método para acceder al formulario
    para editar las marcas.
    """
    q = Marcas.objects.get(pk=id)

    contexto = {'marca': q}

    return render(request, 'run/marcas/editarMarcas.html', contexto)


@decoradorPermitirAE
def updateMarcas(request):
    """Método para acceder a las actualizaciones
    de las marcas.
    """
    if request.method == "POST":
        try:
            marca = Marcas.objects.get(pk=request.POST['id'])
            if request.FILES:
                fss = FileSystemStorage()
                f = request.FILES["imagen"]
                file = fss.save("RUN/fotoMarcas/" + f.name, f)
                # Mi manera de borrar
                import os
                from django.conf import settings
                # base = str()
                # Borrar imagen anterior
                if marca.imagen.url != "/uploads/RUN/fotoMarcas/default.png":
                    fotoVieja = str(settings.BASE_DIR) + marca.imagen.url
                    os.remove(fotoVieja)
                    print("imagen borrada correctamente.")

                # print(f"{settings.BASE_DIR}/{a.foto.url[1:]}")
                # asignamos la foto
                marca.imagen = file

            marca.nombre_marca = request.POST['nombre']
            marca.save()
            messages.success(request, 'Marca actualizada correctamente')
            return redirect('paginaWeb:list_marcas')

        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al intentar editar una marca: {e}')
            return redirect('paginaWeb:list_marcas')
    else:
        messages.warning(request, 'Estás intentado hackear al ganador del SENASOFT? En serio?')
        return redirect('paginaWeb:list_marcas')


# Compras
def verProductos(request):
    """Método para visualizar los 
    productos ofrecidos en la tienda.
    """

    q = Productos.objects.all()

    # aqui hay que manipular los datos que se envian en el contexto
    i = Imagenes.objects.all()
    cont = request.session.get('carrito', False)
    if cont:
        cont = len(cont)
    print(f"el tamaño es {cont}")
    contexto = {'productos': q, 'imagenes': i, 'contador': cont}

    return render(request, 'run/compras/compras.html', contexto)


# Images
def regImagenesForm(request):
    """Formulario para acceder al registro
    de imagenes nuevas para los productos.
    """
    p = Productos.objects.all()
    contexto = {'productos': p}
    return render(request, 'run/imagenes/registrar_imagenes.html', contexto)


def regImagenes(request):
    """Método para guardar las imagenes 
    con su respectivo producto
    """
    if request.method == "POST":
        try:
            if request.FILES:
                # crear instancia de File System Storage
                fss = FileSystemStorage()
                # capturar la foto del formulario
                f = request.FILES["imagen"]
                # cargar archivos al servidor
                file = fss.save("RUN/imagProductos/" + f.name, f)  # Guardar en esta ruta, esta imagen.
            else:
                file = "RUN/imagProductos/default.png"

            q = Imagenes(
                id_imagen=request.POST['idImagen'],
                imagen=file,
                productos=Productos.objects.get(pk=request.POST['producto']),
            )
            q.save()
            messages.success(request, "Imagen guardadada correctamente!!!")
        except Exception as e:
            messages.error(request, f"Ha ocurrido un error {e}")
            return redirect('paginaWeb:reg_imagenes_form')
    else:
        messages.warning(request, "Estás haciendo cosas raras...")

    return redirect('paginaWeb:list_imagenes')


def eliminarImagenes(request, id):
    """Método para eliminar las imagenes
    de los productos.
    """
    try:
        imagenes = Imagenes.objects.get(pk=id)
        from pathlib import Path
        from os import remove, path
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent

        ruta_imagen = str(BASE_DIR) + str(imagenes.imagen.url)

        # Buscamos si la ruta existe
        if path.exists(ruta_imagen):
            # si es diferente a la default la borramos, ya que no podemos borrar la imagen por predeterminado
            if imagenes.imagen.url != "/uploads/RUN/imagProductos/default.png":
                remove(ruta_imagen)
                messages.success(request, "Imagen eliminada correctamente.")
            else:
                print("La foto es la predeterminada")
        imagenes.delete()
        messages.success(request, "Eliminado correctamente")
    except Exception as e:
        messages.error(request, f"Hubo un error al eliminar la imagen : {e}")

    return redirect('paginaWeb:list_imagenes')


def listImagenes(request):
    """Método para listar las imagenes
    """
    q = Imagenes.objects.all()
    contexto = {'imagenes': q}
    return render(request, 'run/imagenes/listar_imagenes.html', contexto)


# Inventario
@decoradorPermitirAE
def registroInventario(request):
    """Método para acceder al formulario
    del registro de los productos.
    """
    q = Marcas.objects.all()
    c = Categorias.objects.all()

    contexto = {'marcas': q, 'categorias': c}

    return render(request, 'run/inventario/registroInventario.html', contexto)


@decoradorPermitirAE
def listarInventario(request):
    """Método para mostrar la lista
    de los productos.
    """
    q = Productos.objects.all()

    contexto = {'productos': q}

    return render(request, 'run/inventario/listarInventario.html', contexto)


@decoradorPermitirAE
def crearInventario(request):
    """Método para registrar productos.
    """
    try:
        q = Productos(
            id_producto=request.POST['codigo'],
            nombre_producto=request.POST['nombreRes'],
            stock=request.POST['stock'],
            precio=request.POST['precio'],
            palabras_clave=request.POST['palabClave'],
            marca=Marcas.objects.get(pk=request.POST['marca']),
            categoria=Categorias.objects.get(pk=request.POST['categoria']),
            descripcion=request.POST['descripcion'],
        )
        q.save()
        messages.success(request, 'Producto agregado correctamente!!!')

    except Exception as e:
        messages.error(request, f'Hubo un problema al intentar agregar un producto: {e}')

    return redirect('paginaWeb:list_inv')


@decoradorPermitirAE
def deleteInventario(request, id):
    """Método para eliminar productos del inventario.
    """
    try:
        producto = Productos.objects.get(pk=id)
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente')
    except Exception as e:
        messages.error(request, f'Hubo un problema al intentareliminar : {e}')

    return redirect('paginaWeb:list_inv')


@decoradorPermitirAE
def updateInventarioForm(request, id):
    """Método para acceder al formulario para
    editar los productos.
    """
    q = Productos.objects.get(pk=id)
    m = Marcas.objects.all()
    marcas = Marcas.objects.get(pk=id)
    c = Categorias.objects.all()
    categorias = Categorias.objects.get(pk=id)

    contexto = {'productos': q, 'marcas': m, 'categorias': c, 'm': marcas, 'c': categorias}
    return render(request, 'run/inventario/editarInventario.html', contexto)


@decoradorPermitirAE
def updateInventario(request):
    """Método para actualizar los productos.
    """
    if request.method == "POST":
        try:
            productos = Productos.objects.get(pk=request.POST['codigo'])

            productos.nombre_producto = request.POST['nombreRes']
            productos.stock = request.POST['stock']
            productos.precio = request.POST['precio']
            productos.palabras_clave = request.POST['palabClave']
            productos.marca = Marcas.objects.get(pk=request.POST['marca'])
            productos.categoria = Categorias.objects.get(pk=request.POST['categoria'])
            productos.descripcion = request.POST['descripcion']

            productos.save()
            messages.success(request, 'Producto correctamente editado')

        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al intenar editar: {e}')
    else:
        messages.warning(request, '¿Estás intentado hackear al ganador del SENASOFT? En serio?')

    return redirect('paginaWeb:list_inv')


# Categorias

@decoradorPermitirAE
def formCategorias(request):
    """Método para acceder al formulario
    de registro de categorias.
    """
    return render(request, 'run/categorias/categoriasForm.html')


@decoradorPermitirAEC
def listarCategorias(request):
    """Método para acceder al formulario
    de registro de categorias.
    """
    q = Categorias.objects.all()
    contexto = {'datos': q}
    return render(request, 'run/categorias/listarCategorias.html', contexto)


@decoradorPermitirAE
def addCategorias(request):
    """Método para añadir categorias.
    """
    try:
        q = Categorias(
            id_categoria=request.POST['id'],
            categoria=request.POST['nombre'],
        )
        q.save()
        messages.success(request, "Categoria guardada Correctamente")
    except Exception as e:
        messages.warning(request, f"Hubo un error guardando la categoria{e}")

    return redirect('paginaWeb:list_categorias')


@decoradorPermitirAE
def deleteCategorias(request, id):
    """Método para eliminar categorias.
    """
    try:
        validation = Productos.objects.filter(categoria=id)
        if validation:
            messages.warning(request, f'Categoria asociada a otros registros, borralos y luego intentarlo de nuevo')
            return redirect('paginaWeb:list_categorias')

        categoria = Categorias.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Categoria eliminada correctamente')
    except Exception as e:
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request, f'La categoría esta vinculada a otros registros, eliminelos y luego vuelva a '
                                    f'intentarlo')
        else:
            messages.error(request, f'Hubo un problema al eliminar una categoria: {e}')

    return redirect('paginaWeb:list_categorias')


@decoradorPermitirAE
def updateCategoriasForm(request, id):
    """Método para acceder al formulario
    para editar las categoras.
    """
    q = Categorias.objects.get(pk=id)

    contexto = {'categoria': q}

    return render(request, 'run/categorias/editarCategorias.html', contexto)


@decoradorPermitirAE
def updateCategorias(request):
    """Método para acceder a las actualizaciones
    de las categorias.
    """
    if request.method == "POST":
        try:
            categoria = Categorias.objects.get(pk=request.POST['id'])
            categoria.categoria = request.POST['categoria']
            categoria.save()
            messages.success(request, 'Categoria actualizada correctamente')
            return redirect('paginaWeb:list_categorias')

        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al intentar editar una categoria: {e}')
            return redirect('paginaWeb:list_categorias')
    else:
        messages.warning(request, 'Estás intentado hackear al ganador del SENASOFT? En serio?')
        return redirect('paginaWeb:list_categorias')


# Ayuda
def ayuda(request):
    """Método para ir al apartado de ayudas.
    """
    return render(request, 'run/ayuda/ayuda.html')


# Carrito
@decoradorPermitirC
def carritoCompras(request):
    """Método para acceder al carrito de compras.
    """
    q = Productos.objects.all()
    contexto = {'datos': q}
    return render(request, 'run/carritoCompras.html', contexto)


@decoradorPermitirC
def addCarrito(request, id):
    """Método para añadir productos 
    al carrito de compras.
    """
    try:
        q = Productos.objects.get(pk=id)
        listaCarrito = request.session.get('carrito', False)

        if listaCarrito:
            listaCarrito.append(id)
            request.session['carrito'] = listaCarrito
        else:
            request.session['carrito'] = [id]

        messages.success(request, 'Producto agregado correctamente al carrito')
    except Exception as e:
        messages.error(request,
                       f'Ha ocurrido un error al agregar el producto al carrito, vuélvalo a intentar mas tarde {e}')

    return redirect('paginaWeb:ver_prod')

@decoradorPermitirC
def addCarritoAjax(request, id):
    """Método para añadir productos
    al carrito de compras.
    """
    try:
        q = Productos.objects.get(pk=id)
        listaCarrito = request.session.get('carrito', False)
        if listaCarrito:
            listaCarrito.append(id)
            request.session['carrito'] = listaCarrito
        else:
            request.session['carrito'] = [id]
        contexto = {'message': "success"}
        return JsonResponse(contexto)
        # messages.success(request, 'Producto agregado correctamente al carrito')
    except Exception as e:
        # messages.error(request,
        #               f'Ha ocurrido un error al agregar el producto al carrito, vuélvalo a intentar mas tarde {e}')
        contexto = {'message': f"Hubo error{e}"}

        return JsonResponse(contexto)


@decoradorPermitirC
def mostrarCarrito(request):
    """Método para mostrar los productos en
    el carrito de compras.
    """
    try:
        carrito = request.session.get('carrito', False)
        listaCarrito = []

        if carrito:
            print(carrito)
            for i in carrito:
                q = Productos.objects.get(pk=i)
                listaCarrito.append(q)

        contexto = {'productos': listaCarrito}

        return render(request, 'run/carritoCompras.html', contexto)
    except Exception as e:
        messages.error(request,
                       f'Ha ocurrido un error al traer los productos del carrito, vuelvalo a intentar mas tarde {e}')
        return redirect('paginaWeb:ver_prod')


@decoradorPermitirC
def vaciarCarrito(request):
    """Método para vaciar el carrito
    de compras.
    """
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
    """Método para elminar productos
    del carrito de compras.
    """
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


# Admin - Roles
@decoradorPermitirAE
def listRoles(request):
    """Método para listar los roles.
    """
    q = Roles.objects.all()
    contexto = {'roles': q}
    return render(request, 'run/roles/listarRoles.html', contexto)


@decoradorPermitirA
def regRolesForm(request):
    """Método para acceder al formulario
    para listar los roles.
    """
    return render(request, 'run/roles/registroRoles.html')


@decoradorPermitirA
def rolRegistro(request):
    """Método para registrar roles.
    """
    if request.method == 'POST':
        try:
            q = Roles(
                id_roles=request.POST['idRol'],
                nombre_rol=request.POST['nameRol'],
                descripcion=request.POST['descripcion'],
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
    """Método para eliminar roles.
    """
    try:
        rol = Roles.objects.get(pk=id)
        rol.delete()
        messages.success(request, 'Rol eliminado correctamente')
    except Exception as e:
        messages.error(request, f'Hubo un error al intentar eliminar un rol: {e}')

    return redirect('paginaWeb:list_roles')


@decoradorPermitirA
def updateRolForm(request, id):
    """Método para acceder al formulario
    para editar los roles.
    """
    q = Roles.objects.get(pk=id)
    contexto = {'roles': q}
    return render(request, 'run/roles/editarRoles.html', contexto)


@decoradorPermitirA
def updateRol(request):
    """Método para actualizar los roles.
    """
    if request.method == 'POST':
        try:
            roles = Roles.objects.get(pk=request.POST['idRol'])

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


# Ventas
@decoradorPermitirAE
def formVentas(request):
    """Método para acceder al fomulario
    de las ventas.
    """
    p = Personas.objects.all()
    contexto = {'personas': p}
    return render(request, 'run/ventas/ventasForm.html', contexto)


@decoradorPermitirAE
def listarVentas(request):
    """Método para listar las ventas
    """
    q = Ventas.objects.all()
    contexto = {'datos': q}
    return render(request, 'run/ventas/listarVentas.html', contexto)


@decoradorPermitirAE
def addVentas(request):
    """Método para añadir ventas.
    """
    if request.method == 'POST':
        try:
            ventaExistente = Ventas.objects.filter(id_venta=request.POST['id_venta'])
            if ventaExistente:
                messages.error(request, "id de Venta ya registrada, ingrese una diferente por favor")
                return redirect('paginaWeb:form_ventas')
            else:
                q = Ventas(
                    id_venta=request.POST['id_venta'],
                    direccion=request.POST['direccion'],
                    persona=Personas.objects.get(pk=request.POST['persona']),
                )
                q.save()
                messages.success(request, "Venta registrada exitosamente")
                return redirect('paginaWeb:list_ventas')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:form_ventas')
    else:
        messages.warning(request, "No hay datos para registrar, que estás tratando de hacer?")
        return redirect('paginaWeb:list_ventas')


@decoradorPermitirAE
def deleteVentas(request, id):
    """Método para eliminar las ventas.
    """
    try:
        venta = Ventas.objects.get(pk=id)
        venta.delete()
        messages.success(request, 'Venta eliminada correctamente')
        return redirect('paginaWeb:list_ventas')
    except Exception as e:
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request,
                           f'La venta esta vinculada a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_ventas')
        else:
            messages.error(request, f'Hubo un problema al eliminar una venta: {e}')
            return redirect('paginaWeb:list_ventas')


@decoradorPermitirAE
def updateVentasForm(request, id):
    """Método para acceder al formulario para
    actualizar las ventas.
    """
    q = Ventas.objects.get(pk=id)
    p = Personas.objects.all()

    contexto = {'ventas': q, 'personas': p}
    return render(request, 'run/ventas/editarVentas.html', contexto)


@decoradorPermitirAE
def updateVentas(request):
    """Método para actualizar las ventas.
    """
    if request.method == "POST":
        try:
            venta = Ventas.objects.get(id_venta=request.POST['id_venta'])
            venta.direccion = request.POST['direccion']
            venta.persona = Personas.objects.get(pk=request.POST['persona'])
            venta.save()
            messages.success(request, "Venta actualizada exitosamente")
            return redirect('paginaWeb:list_ventas')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:upd_ventas_form')


# PedidosProductos
@decoradorPermitirA
def formPedidos(request):
    """Método para acceder al formulario
    para crear pedidos.
    """
    productos = Productos.objects.all()
    ventas = Ventas.objects.all()
    contexto = {'productos': productos, 'ventas': ventas}
    return render(request, 'run/pedidos/pedidosForm.html', contexto)


@decoradorPermitirA
def listarPedidos(request):
    """Método para listar los pedidos.
    """
    q = Pedidos.objects.all()
    contexto = {'datos': q}
    return render(request, 'run/pedidos/listarPedidos.html', contexto)


@decoradorPermitirA
def addPedidos(request):
    """Método para añadir nuevos pedidos.
    """
    if request.method == 'POST':
        try:
            pedidoExistente = Pedidos.objects.filter(id_pedido=request.POST['pedido'])
            productoExistente = Productos.objects.filter(id_producto=request.POST['producto'])
            ventaExistente = Ventas.objects.filter(id_venta=request.POST['venta'])
            if pedidoExistente:
                messages.error(request, "id de pedido ya existente, ingrese uno diferente")
                return redirect('paginaWeb:form_pedidos')
            elif not productoExistente:
                messages.error(request, "producto inexistente, ingrese uno diferente")
                return redirect('paginaWeb:form_pedidos')
            elif not ventaExistente:
                messages.error(request, "venta inexistente, ingrese una que exista")
                return redirect('paginaWeb:form_pedidos')

            q = Pedidos(
                id_pedido=request.POST['pedido'],
                producto=Productos.objects.get(pk=request.POST['producto']),
                venta=Ventas.objects.get(pk=request.POST['venta']),
                cantidad=request.POST['cantidad'],
            )
            q.save()
            messages.success(request, "Pedido registrado exitosamente")
            return redirect('paginaWeb:list_pedidos')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:form_pedidos')
    else:
        messages.warning(request, "No hay datos para registrar, que estas tratando de hacer?")
        return redirect('paginaWeb:list_pedidos')


@decoradorPermitirA
def deletePedidos(request, id):
    """Método para eliminar pedidos.
    """
    try:
        pedido = Pedidos.objects.get(id_pedido=id)
        pedido.delete()
        messages.success(request, 'pedido eliminado correctamente')
        return redirect('paginaWeb:list_pedidos')
    except Exception as e:
        messages.error(request, f'Hubo un problema al eliminar un pedido: {e}')
        return redirect('paginaWeb:list_pedidos')


@decoradorPermitirA
def updatePedidosForm(request, id):
    """Método para acceder al
    formulario para editar pedidos.
    """
    pedido = Pedidos.objects.get(pk=id)
    productos = Productos.objects.all()
    ventas = Ventas.objects.all()
    contexto = {'pedido': pedido, 'productos': productos, 'ventas': ventas}
    return render(request, 'run/pedidos/editarPedidos.html', contexto)


@decoradorPermitirA
def updatePedidos(request):
    """Método para actualizar los pedidos.
    """
    if request.method == "POST":
        try:
            pedido = Pedidos.objects.get(id_pedido=request.POST['id_pedido'])
            productoExistente = Productos.objects.filter(id_producto=request.POST['producto'])
            ventaExistente = Ventas.objects.filter(id_venta=request.POST['venta'])
            if not productoExistente:
                messages.error(request, "id de producto inexistente, ingrese uno que exista")
                return redirect('paginaWeb:upd_pedidos_form')
            elif not ventaExistente:
                messages.error(request, "id de venta inexistente, ingrese una que exista")
                return redirect('paginaWeb:upd_pedidos_form')

            pedido.producto = Productos.objects.get(pk=request.POST['producto'])
            pedido.venta = Ventas.objects.get(pk=request.POST['venta'])
            pedido.cantidad = request.POST['cantidad']

            pedido.save()
            messages.success(request, "pedido registrado exitosamente")
            return redirect('paginaWeb:list_pedidos')
        except Exception as e:
            messages.error(request, f"Hubo un error en el proceso de registro: {e}")
            return redirect('paginaWeb:upd_pedidos_form')


# MediosDePago
@decoradorPermitirA
def listMediosPagos(request):
    """Método para listar
    los medios de pagos.
    """
    q = MediosDePagos.objects.all()
    contexto = {'medios': q}
    return render(request, 'run/mediosPagos/listarMediosPagos.html', contexto)


@decoradorPermitirA
def formMediosPagos(request):
    """Método para acceder al formulario
    de los medios de pagos.
    """
    return render(request, 'run/mediosPagos/mediosPagosForm.html')


@decoradorPermitirA
def addMediosPagos(request):
    """Método para añadir
    los medios de pago.
    """
    if request.method == 'POST':
        try:
            q = MediosDePagos(
                id_medio_pago=request.POST['idMedio'],
                nombre_medio_pago=request.POST['nombreMedio'],
                estado_medio_pago=request.POST['estado'],
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
    """Método para eliminar
    los medios de pagos.
    """
    try:
        medioPago = MediosDePagos.objects.get(pk=id)
        medioPago.delete()
        messages.success(request, 'Medio de pago eliminado correctamente')
        return redirect('paginaWeb:list_mediosPagos')
    except Exception as e:
        if str(e) == "FOREIGN KEY constraint failed":
            messages.error(request,
                           f'El medio de pago está vinculado a otros registros, eliminelos y luego vuelva a intentarlo')
            return redirect('paginaWeb:list_mediosPagos')
        else:
            messages.error(request, f'Hubo un problema al eliminar un medio de pago: {e}')
            return redirect('paginaWeb:list_mediosPagos')


@decoradorPermitirA
def updateMediosPagosForm(request, id):
    """Método para acceder al formualrio
    de los medios de pagos.
    """
    q = MediosDePagos.objects.get(pk=id)
    a = MediosDePagos.objects.all()
    contexto = {'medios': q, 'medPagos': a}
    return render(request, 'run/mediosPagos/editarMedioPago.html', contexto)


@decoradorPermitirA
def updateMediosPagos(request):
    """Método para actualizar
    los medios de pagos.
    """
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


# Pagos
@decoradorPermitirAE
def listPagos(request):
    """Método para listar los pagos.
    """
    q = Pagos.objects.all()
    contexto = {'pagos': q}
    return render(request, 'run/pagos/listarPagos.html', contexto)


@decoradorPermitirA
def formPagos(request):
    """Método para acceder al formulario
    para crear pagos.
    """
    q = MediosDePagos.objects.all()
    v = Ventas.objects.all()
    contexto = {'medPagos': q, 'ventas': v}
    return render(request, 'run/pagos/pagosForm.html', contexto)


@decoradorPermitirA
def addPagos(request):
    """Método para crear nuevos pagos.
    """
    if request.method == 'POST':
        try:
            q = Pagos(
                id_pago=request.POST['idPago'],
                venta=Ventas.objects.get(pk=request.POST['venta']),
                medio_pago=MediosDePagos.objects.get(pk=request.POST['medioPago']),
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
    """Método para eliminar pagos
    """
    try:
        pagos = Pagos.objects.get(pk=id)
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
    """Método para acceder al formulario
     para actualizar pagos.
    """
    q = Pagos.objects.get(pk=id)
    v = Ventas.objects.all()
    a = MediosDePagos.objects.all()
    contexto = {'pagos': q, 'medPagos': a, 'ventas': v}
    return render(request, 'run/pagos/editarPagos.html', contexto)


@decoradorPermitirA
def updatePagos(request):
    """Métodos para actualizar los pagos.
    """
    if request.method == "POST":
        try:
            pagos = Pagos.objects.get(id_pago=request.POST['idPago'])

            pagos.medio_pago = MediosDePagos.objects.get(pk=request.POST['medioPago'])
            pagos.fecha_pagos = request.POST['fecha']
            pagos.save()

            messages.success(request, "Actualizado correctamente")
        except Exception as e:
            messages.error(request, f"Hubo un error al momento de actualizar: {e}")
    else:
        messages.warning(request, "No sabemos por donde se está metiendo pero no puedes avanzar, puerco")

    return redirect('paginaWeb:list_pagos')
