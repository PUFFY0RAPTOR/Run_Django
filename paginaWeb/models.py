
from django.db import models


# Create your models here.

class Roles(models.Model):
    id_roles = models.IntegerField(primary_key=True)
    nombre_rol = models.CharField(max_length=100)
    descripcion = models.TextField(default="Descripción del rol...")

    def __str__(self):
        return self.nombre_rol


class Marcas(models.Model):
    id_marca = models.IntegerField(primary_key=True)
    nombre_marca = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='RUN/fotoMarcas', default='RUN/fotoMarcas/default.png')
    def __str__(self):
        return self.nombre_marca


class Personas(models.Model):
    cedula = models.IntegerField(primary_key=True)
    foto = models.ImageField(upload_to='RUN/fotoUsuario', default='RUN/fotoUsuario/defaultFoto.png')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    celular = models.CharField(max_length=12)
    fecha_nacimiento = models.DateField(default='2000-01-01')
    direccion = models.CharField(max_length=200)
    # Será tipo de usuario, que puede ser cliente o empleado
    correo = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=235)
    roles = models.ForeignKey(Roles, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre


class Categorias(models.Model):
    id_categoria = models.IntegerField(primary_key=True)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria

class Productos(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    stock = models.FloatField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion = models.TextField(default="")
    palabras_clave = models.CharField(max_length=100)
    marca = models.ForeignKey(Marcas, on_delete=models.DO_NOTHING)
    categoria = models.ForeignKey(Categorias, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id_producto}"


class Imagenes(models.Model):
    id_imagen = models.IntegerField(primary_key=True)
    imagen = models.ImageField(upload_to='RUN/imagProductos', default='RUN/imagProductos/default.png')
    productos = models.ForeignKey(Productos, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.imagen.url}"


class Ventas(models.Model):
    id_venta = models.IntegerField(primary_key=True)
    fecha_envio = models.DateTimeField(auto_now=True)
    direccion = models.CharField(max_length=100)
    persona = models.ForeignKey(Personas, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.fecha_envio}"


class Pedidos(models.Model):
    id_pedido = models.IntegerField(primary_key=True)
    venta = models.ForeignKey(Ventas, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Productos, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.cantidad}"


class MediosDePagos(models.Model):
    id_medio_pago = models.IntegerField(primary_key=True)
    nombre_medio_pago = models.CharField(max_length=50)
    estado_medio_pago = models.CharField(max_length=35)

    def __str__(self):
        return self.nombre_medio_pago


class Pagos(models.Model):
    id_pago = models.IntegerField(primary_key=True)
    venta = models.ForeignKey(Ventas, on_delete=models.DO_NOTHING)
    medio_pago = models.ForeignKey(MediosDePagos, on_delete=models.DO_NOTHING)
    fecha_pagos = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.fecha_pagos)
