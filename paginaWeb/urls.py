from django.urls import path
from . import views

app_name="paginaWeb"
urlpatterns = [
    path('', views.index, name='index'),

    #Login
    path('loginForm/', views.loginForm, name='login_form'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    #clientes
    path('registroClientes/', views.registro, name='registro'),
    path('guardarClientes/', views.guardarCliente, name='guardarCliente'),
    path('eliminarCliente/<int:id>', views.eliminarCliente, name='delCliente'),
    path('clienteEditar/<int:id>', views.buscarClienteEditar, name="upd_clientes_form"),
    path('updateCliente/', views.updateCliente, name='updCliente'),
    path('listarClientes/', views.listarClientes, name='list_usu'),


    #Empleados
    path('formuEmpleados/', views.formEmpleados, name='form_empleados'),
    path('listarEmpleados/', views.listarEmpleados, name='list_empleados'),
    path('addEmpleados/', views.addEmpleados, name='add_empleados'),
    path('elimEmpleados/<id>', views.deleteEmpleados, name='del_empleados'),
    path('updateEmpleadosForm/<id>', views.updateEmpleadosForm, name='upd_empleados_form'),
    path('updateEmpleados/', views.updateEmpleados, name='upd_empleados'),

    #Usuarios
    path('formuUsuarios/', views.formUsuarios, name='form_usuarios'),
    path('listarUsuarios/', views.listarUsuarios, name='list_usuarios'),
    path('addUsuarios/', views.addUsuarios, name='add_usuarios'),
    path('elimUsuarios/<id>', views.deleteUsuarios, name='del_usuarios'),
    path('updateUsuariosForm/<id>', views.updateUsuariosForm, name='upd_usuarios_form'),
    path('updateUsuarios/', views.updateUsuarios, name='upd_usuarios'),

    #Ventas -apenas comenzando, prioridad a otras tablas 
    # path('formuVentas/', views.formVentas, name='form_ventas'),
    # path('listarVentas/', views.listarVentas, name='list_ventas'),
    # path('addVentas/', views.addVentas, name='add_ventas'),
    # path('elimVentas/<id>', views.deleteVentas, name='del_ventas'),
    # path('updateVentasForm/<id>', views.updateVentasForm, name='upd_ventas_form'),
    # path('updateVentas/', views.updateVentas, name='upd_ventas'),


    #Pedidos
    path('formuPedidos/', views.formPedidos, name='form_pedidos'),
    path('listarPedidos/', views.listarPedidos, name='list_pedidos'),
    path('addPedidos/', views.addPedidos, name='add_pedidos'),
    path('elimPedidos/<id>', views.deletePedidos, name='del_pedidos'),
    path('updatePedidosForm/<id>', views.updatePedidosForm, name='upd_pedidos_form'),
    path('updatePedidos/', views.updatePedidos, name='upd_pedidos'),

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


    #Envios
    path('listarEnvios/', views.listEnvios, name='list_envios'),
    path('FormEnvios/', views.formEnvios, name='form_envios'),
    path('addEnvios/', views.addEnvios, name='add_envios'),
    path('deleteEnvios/<int:id>', views.deleteEnvios, name='del_envios'),
    path('updateEnviosForm/<int:id>', views.updateEnviosForm, name='upd_envios_form'),
    path('updateEnvios/', views.updateEnvios, name='upd_envios'),
    

    #MediosDePago
    path('listarMediosPago/', views.listMediosPagos, name='list_mediosPagos'),
    path('formMediosPago/', views.formMediosPagos, name='form_mediosPagos'),
    path('addMedioPago/', views.addMediosPagos, name='add_medioPago'),
    path('deleteMedioPago/<int:id>', views.deleteMediosPagos, name='del_mediosPagos'),
    path('updateMedioPagoForm/<int:id>', views.updateMediosPagosForm, name='upd_mediosPagos_form'),
    path('updateMedioPagos/', views.updateMediosPagos, name='upd_mediosPagos'),
]