from django.urls import path
from . import views

app_name="paginaWeb"
urlpatterns = [
    path('', views.index, name='index'),

    #Login
    path('login/', views.login, name='login'),

    #Registros usuarios
    path('registro/', views.registro, name='registro'),
    path('guardarUsu/', views.guardarCliente, name='guardarCliente'),
    path('eliminarCliente/<int:id>', views.eliminarCliente, name='delCliente'),
    path('updateCliente/', views.updateCliente, name='updCliente'),
    path('listarUsuarios/', views.listarUsuarios, name='list_usu'),

    #Repuestos
    path('listarRepuestos/', views.listarRepuestos, name='list_rep'),

    #Compras
    path('verProductos/', views.verProductos, name='ver_prod'),

    #Inventario
    path('regInventario/', views.registroInventario, name='reg_inv'),
    path('inventario/', views.listarInventario, name='list_inv'),
    path('crearInv/', views.crearInventario, name='crear_inv'),

    #Ayuda
    path('ayuda/', views.ayuda, name='ayuda'),

    #Marcas
    path('marcas/', views.marcas, name='marcas'),

    #Carrito
    path('carritoCompras/', views.carritoCompras, name='carrito'),


]