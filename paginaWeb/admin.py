from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Marcas)
class MarcasAdmin(admin.ModelAdmin):
    list_display = ('id_marca','nombre_marca',)
    search_fields = ['id_marca', 'nombre_marca',]


@admin.register(Roles)
class MarcasAdmin(admin.ModelAdmin):
    list_display = ('id_roles','nombre_rol', 'descripcion')
    search_fields = ['id_roles', 'nombre_rol','descripcion']


@admin.register(Categorias)
class MarcasAdmin(admin.ModelAdmin):
    list_display = ('id_categoria','categoria',)
    search_fields = ['id_categoria', 'categoria',]


@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('id_producto','nombre_producto', 'stock', 'precio', 'marca', 'descripcion', 'palabras_clave', 'marca', 'verImagen')
    search_fields = ['id_producto','nombre_producto', 'stock', 'precio', 'marca', 'descripcion', 'palabras_clave', 'marca']
    def verImagen(self, obj):
        #general codigo html en el admin
        from django.utils.html import format_html
        producto = obj.id_producto
        h = Imagenes.objects.filter(productos = producto)
        s = ""
        for i in h:
            imagen = i.imagen.url
            s +="<a href='"+str(imagen)+"' target='_blank' ><img src='"+str(imagen)+"'  width='20%' /></a>"
        return format_html(s)

@admin.register(Personas)
class PersonasAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'verFoto', 'nombre', 'apellido', 'celular', 'fecha_nacimiento', 'direccion', 'tipo', 'correo', 'contrasena', 'roles')
    search_fields = ['cedula', 'nombre', 'apellido', 'celular', 'fecha_nacimiento', 'direccion', 'tipo', 'correo', 'roles']

    def verFoto(self, obj):
        #general codigo html en el admin
        from django.utils.html import format_html
        imagen = obj.foto.url
        return format_html(
            f"<a href='{imagen}' target='_blank' ><img src='{imagen}'  width='20%' /></a>"
        )

@admin.register(Imagenes)
class ImagenesAdmin(admin.ModelAdmin):
    list_display = ('id_imagen', 'verImagen', 'productos')
    search_fields = ['id_imagen', 'productos']

    def verImagen(self, obj):
        #general codigo html en el admin
        from django.utils.html import format_html
        imagen = obj.imagen.url
        return format_html(
            f"<a href='{imagen}' target='_blank' ><img src='{imagen}'  width='20%' /></a>"
        )


@admin.register(PedidosProductos)
class PedidosProductosAdmin(admin.ModelAdmin):
    list_display = ('id_pedidos_productos','ventas', 'producto', 'cantidad')
    search_fields = ['id_pedidos_productos','ventas__venta', 'producto_producto', 'cantidad']


@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('id_venta','fecha_envio', 'direccion', 'persona')
    search_fields = ['id_venta','fecha_envio', 'direccion', 'persona']


@admin.register(MediosDePagos)
class MediosDePagosAdmin(admin.ModelAdmin):
    list_display = ('id_medio_pago','nombre_medio_pago', 'estado_medio_pago')
    search_fields = ['id_medio_pago','nombre_medio_pago', 'estado_medio_pago']


@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display = ('id_pago','venta' ,'medio_pago', 'fecha_pagos')
    search_fields = ['id_pago','venta', 'medio_pago', 'fecha_pagos']

