from django.urls import path
from . import views

app_name="paginaWeb"
urlpatterns = [
    path('', views.index, name='index'),

    #Login
    path('loginForm/', views.loginForm, name='login_form'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    #Registros usuarios
    path('registro/', views.registro, name='registro'),
    path('guardarUsu/', views.guardarCliente, name='guardarCliente'),
    path('eliminarCliente/<int:id>', views.eliminarCliente, name='delCliente'),
    path('updateCliente/', views.updateCliente, name='updCliente'),
    path('listarUsuarios/', views.listarUsuarios, name='list_usu'),

    #Marcas
    path('formuMarcas/', views.formMarcas, name='form_marcas'),
    path('listarMarcas/', views.listarMarcas, name='list_marcas'),
    path('addMarcas/', views.addMarcas, name='add_marcas'),
    path('elimMarcas/<int:id>', views.deleteMarcas, name='del_marcas'),
    path('updateMarcasForm/<int:id>', views.updateMarcasForm, name='upd_marcas_form'),
    path('updateMarcas/', views.updateMarcas, name='upd_marcas'),

    #Compras
    path('verProductos/', views.verProductos, name='ver_prod'),

    #Inventario
    path('regInventario/', views.registroInventario, name='reg_inv'),
    path('inventario/', views.listarInventario, name='list_inv'),
    path('crearInv/', views.crearInventario, name='crear_inv'),
    path('elimInv/<int:id>', views.deleteInventario, name='del_inv'),
    path('updateInvForm/<int:id>', views.updateInventarioForm, name='upd_inv_form'),
    path('updateInv/', views.updateInventario, name='upd_inv'),


    #Ayuda
    path('ayuda/', views.ayuda, name='ayuda'),

    #Marcas
    path('marcas/', views.marcas, name='marcas'),

    #Carrito
    path('carritoCompras/', views.carritoCompras, name='carrito'),


    #Admin - Roles
    path('listarRoles/', views.listRoles, name='list_roles'),
    path('regRolesForm/', views.regRolesForm, name='reg_roles_form'),
    path('registroRoles/', views.rolRegistro, name='reg_roles'),
    path('deleteRoles/<int:id>', views.deleteRol, name='del_roles'),
    path('updateRolesForm/<int:id>', views.updateRolForm, name='upd_roles_form'),
    path('updateRoles/', views.updateRol, name='upd_roles'),


]