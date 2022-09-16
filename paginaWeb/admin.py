from django.contrib import admin
from .models import Roles, Marcas, Usuarios, Empleados, Clientes, Pedidos, Marcas, Productos, PedidosProductos, Envios, Ventas, Historial, MediosDePagos, Pagos
# Register your models here.

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('id_roles', 'nombre_rol')
    search_fields = ['id_roles', 'nombre_rol']
    
""" @admin.register(Permisos)
class PermisosAdmin(admin.ModelAdmin):
    list_display = ('nombre_permiso', 'description')
    search_fields = ['nombre_permiso', 'description']    """
    
@admin.register(Marcas)
class MarcasAdmin(admin.ModelAdmin):
    list_display = ('id_marca','nombre_marca',)
    search_fields = ['id_marca', 'nombre_marca',]

""" @admin.register(RolesPermisos)
class RolesPermisosAdmin(admin.ModelAdmin):
    list_display = ('id_roles_permisos','roles','permisos',)
    search_fields = ['id_roles_permisos',] """

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id_correo','roles')
    search_fields = ['id_correo', 'roles__roles']

@admin.register(Empleados)
class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ('id_empleado','nombre_empleado', 'apellido_empleado', 'celular_empleado', 'fecha_nacimiento', 'eps', 'Correo_Usuario')
    search_fields = ['id_empleado', 'nombre_empleado', 'apellido_empleado', 'celular_empleado', 'fecha_nacimiento', 'eps', 'usuarios__correo']

    def Correo_Usuario(obj, self):
        return self.correo.id_correo

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('id_cliente','nombre_cliente', 'apellido_cliente', 'celular_cliente', 'fecha_nacimiento', 'direccion', 'Correo_Usuario')
    search_fields = ['id_cliente', 'nombre_cliente', 'apellido_cliente', 'celular_cliente', 'fecha_nacimiento', 'direccion', 'usuarios__correo']

    def Correo_Usuario(obj, self):
        return self.correo.id_correo

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ('id_pedido','cliente')
    search_fields = ['id_pedido','cliente__cliente']

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('id_producto','nombre_producto', 'stock', 'precio', 'marca')
    search_fields = ['id_producto','nombre_producto', 'stock', 'precio', 'marca']

@admin.register(PedidosProductos)
class PedidosProductosAdmin(admin.ModelAdmin):
    list_display = ('id_pedidos_productos','pedido', 'producto')
    search_fields = ['id_pedidos_productos','pedido__pedido', 'producto_producto']

@admin.register(Envios)
class EnviosAdmin(admin.ModelAdmin):
    list_display = ('id_envios','fecha_envio', 'direccion_envio')
    search_fields = ['id_envios','fecha_envio', 'direccion_envio']

@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('id_venta','pedido', 'envio', 'fecha')
    search_fields = ['id_venta','pedido_pedido', 'envio_envio', 'fecha']

@admin.register(MediosDePagos)
class MediosDePagosAdmin(admin.ModelAdmin):
    list_display = ('id_medio_pago','nombre_medio_pago', 'estado_medio_pago')
    search_fields = ['id_medio_pago','nombre_medio_pago', 'estado_medio_pago']

@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display = ('id_pago','medio_pago', 'fecha_pagos')
    search_fields = ['id_pago','medio_pago', 'fecha_pagos']

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('id_historial','venta', 'pago')
    search_fields = ['id_historial','venta', 'pago']

"""
"""