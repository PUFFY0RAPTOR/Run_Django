from django.db import models

# Create your models here.

class Roles(models.Model):
    id_roles = models.IntegerField(primary_key=True)
    nombre_rol = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre_rol

class Marcas(models.Model):
    id_marca = models.IntegerField(primary_key=True)
    nombre_marca = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre_marca
       
""" class Permisos(models.Model):
    id_permiso = models.IntegerField(primary_key=True)
    nombre_permiso = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    #intermedia = models.ManyToManyField(Roles,blank=True)

    def __str__(self):
        return self.nombre_permiso

class RolesPermisos(models.Model):
    id_roles_permisos = models.IntegerField(primary_key=True)
    roles = models.ForeignKey(Roles, on_delete = models.DO_NOTHING)
    permisos = models.ForeignKey(Permisos, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.nombre_rol """

class Usuarios(models.Model):
    id_correo = models.CharField(max_length=150, primary_key=True)
    contrasena = models.CharField(max_length=14)
    roles = models.ForeignKey(Roles, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.id_correo

class Empleados(models.Model):
    id_empleado = models.IntegerField(primary_key=True)
    nombre_empleado = models.CharField(max_length=100)
    apellido_empleado = models.CharField(max_length=100)
    celular_empleado = models.IntegerField()
    fecha_nacimiento = models.DateField(default='2000-01-01')
    eps = models.CharField(max_length=50)
    correo = models.ForeignKey(Usuarios, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.nombre_empleado

class Clientes(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    apellido_cliente = models.CharField(max_length=100)
    celular_cliente = models.IntegerField()
    fecha_nacimiento = models.DateField(default='2000-01-01')
    direccion = models.CharField(max_length=125)
    correo = models.ForeignKey(Usuarios, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.nombre_cliente

class Pedidos(models.Model):
    id_pedido = models.IntegerField(primary_key=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Pedidos"

class Marcas(models.Model):
    id_marca = models.IntegerField(primary_key=True)
    nombre_marca = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_marca

class Productos(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    stock = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    marca = models.ForeignKey(Marcas, on_delete = models.DO_NOTHING)
    descripcion = models.TextField(default="")

    def __str__(self):
        return self.nombre_producto

class PedidosProductos(models.Model):
    id_pedidos_productos = models.IntegerField(primary_key=True)
    pedido = models.ForeignKey(Pedidos, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Productos, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Pedidos Productos"

class Envios(models.Model):
    id_envios = models.IntegerField(primary_key=True)
    fecha_envio = models.DateField(default="2000-01-01")
    direccion_envio = models.CharField(max_length=100)

    def __str__(self):
        return self.direccion_envio

class Ventas(models.Model):
    id_venta = models.IntegerField(primary_key=True)
    pedido = models.ForeignKey(Pedidos, on_delete=models.DO_NOTHING)
    envio = models.ForeignKey(Envios, on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Ventas"

class MediosDePagos(models.Model):
    id_medio_pago = models.IntegerField(primary_key=True)
    nombre_medio_pago = models.CharField(max_length=50)
    estado_medio_pago = models.CharField(max_length=35)

    def __str__(self):
        return self.nombre_medio_pago

class Pagos(models.Model):
    id_pago = models.IntegerField(primary_key=True)
    medio_pago = models.ForeignKey(MediosDePagos, on_delete=models.DO_NOTHING)
    fecha_pagos = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fecha_pagos

class Historial(models.Model):
    id_historial = models.IntegerField(primary_key=True)
    venta = models.ForeignKey(Ventas, on_delete=models.DO_NOTHING)
    pago = models.ForeignKey(Pagos, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Historial"

"""          
"""
