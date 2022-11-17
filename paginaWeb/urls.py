from django.urls import path
from . import views
from .views import decoradorPermitirAE, decoradorDenegarAEC, decoradorPermitirAEC, decoradorPermitirA, decoradorPermitirC, decoradorPermitirAC

app_name="paginaWeb"
urlpatterns = [
    path('', views.index, name='index'),

    #Login
    path('loginForm/', decoradorDenegarAEC(views.loginForm), name='login_form'),
    path('login/', decoradorDenegarAEC(views.login), name='login'),
    path('logout/', decoradorPermitirAEC(views.logout), name='logout'),

    #Nuevo código
    path('personasForm/', views.registrarPersonasForm, name='personas_form'),
    path('registrarPersonas/', views.registrarPersonas, name='reg_personas'),
    


    #clientes
    path('registroClientes/', decoradorDenegarAEC(views.registro), name='registro'),
    path('guardarClientes/', decoradorDenegarAEC(views.guardarCliente), name='guardarCliente'),
    path('eliminarCliente/<int:id>', decoradorPermitirAC(views.eliminarCliente), name='delCliente'),
    path('eliminarCliente/', views.sinId, name='del_cliente_sin_id'),
    path('clienteEditar/<int:id>', decoradorPermitirAEC(views.buscarClienteEditar), name="upd_clientes_form"),
    path('clienteEditar/', views.sinId, name='upd_cliente_sin_id'),
    path('updateCliente/', decoradorPermitirC(views.updateCliente), name='updCliente'),
    path('listarClientes/', decoradorPermitirAE(views.listarClientes), name='list_usu'),


    #Empleados
    path('formuEmpleados/', decoradorPermitirA(views.formEmpleados), name='form_empleados'),
    path('listarEmpleados/', decoradorPermitirA(views.listarEmpleados), name='list_empleados'),
    path('addEmpleados/', decoradorPermitirA(views.addEmpleados), name='add_empleados'),
    path('elimEmpleados/<id>', decoradorPermitirA(views.deleteEmpleados), name='del_empleados'),
    path('elimEmpleados/', views.sinId, name='del_empleados_sin_id'),
    path('updateEmpleadosForm/<id>', decoradorPermitirA(views.updateEmpleadosForm), name='upd_empleados_form'),
    path('updateEmpleadosForm/', views.sinId, name='upd_empleados_form_sin_id'),
    path('updateEmpleados/', decoradorPermitirA(views.updateEmpleados), name='upd_empleados'),

    #Usuarios
    path('formuUsuarios/', decoradorPermitirA(views.formUsuarios), name='form_usuarios'),
    path('listarUsuarios/', decoradorPermitirA(views.listarUsuarios), name='list_usuarios'),
    path('addUsuarios/', decoradorPermitirA(views.addUsuarios), name='add_usuarios'),
    path('elimUsuarios/<id>', decoradorPermitirA(views.deleteUsuarios), name='del_usuarios'),
    path('elimUsuarios/', views.sinId, name='del_usuarios_sin_id'),
    path('updateUsuariosForm/<id>', decoradorPermitirA(views.updateUsuariosForm), name='upd_usuarios_form'),
    path('updateUsuariosForm/', views.sinId, name='upd_usuarios_form_sin_id'),
    path('updateUsuarios/', decoradorPermitirA(views.updateUsuarios), name='upd_usuarios'),

    #Ventas 
    path('formuVentas/', decoradorPermitirAE(views.formVentas), name='form_ventas'),
    path('listarVentas/', decoradorPermitirAE(views.listarVentas), name='list_ventas'),
    path('addVentas/', decoradorPermitirAE(views.addVentas), name='add_ventas'),
    path('elimVentas/<id>', decoradorPermitirAE(views.deleteVentas), name='del_ventas'),
    path('elimVentas/', views.sinId, name='del_ventas_sin_id'),
    path('updateVentasForm/<id>', decoradorPermitirAE(views.updateVentasForm), name='upd_ventas_form'),
    path('updateVentasForm/', views.sinId, name='upd_ventas_form_sin_id'),
    path('updateVentas/', decoradorPermitirAE(views.updateVentas), name='upd_ventas'),


    #Historial 
    path('formuHistorial/', decoradorPermitirA(views.formHistorial), name='form_historial'),
    path('listarHistorial/', decoradorPermitirAE(views.listarHistorial), name='list_historial'),
    path('addHistorial/', decoradorPermitirA(views.addHistorial), name='add_historial'),
    path('elimHistorial/<id>', decoradorPermitirA(views.deleteHistorial), name='del_historial'),
    path('elimHistorial/', views.sinId, name='del_historial_sin_id'),
    path('updateHistorialForm/<id>', decoradorPermitirA(views.updateHistorialForm), name='upd_historial_form'),
    path('updateHistorialForm/', views.sinId, name='upd_historial_form_sin_id'),
    path('updateHistorial/', decoradorPermitirA(views.updateHistorial), name='upd_historial'),


    #Pedidos
    path('formuPedidos/', decoradorPermitirAE(views.formPedidos), name='form_pedidos'),
    path('listarPedidos/', decoradorPermitirAE(views.listarPedidos), name='list_pedidos'),
    path('addPedidos/', decoradorPermitirAE(views.addPedidos), name='add_pedidos'),
    path('elimPedidos/<id>', decoradorPermitirAE(views.deletePedidos), name='del_pedidos'),
    path('elimPedidos/', views.sinId, name='del_pedidos_sin_id'),
    path('updatePedidosForm/<id>', decoradorPermitirAE(views.updatePedidosForm), name='upd_pedidos_form'),
    path('updatePedidosForm/', views.sinId, name='upd_pedidos_form_sin_id'),
    path('updatePedidos/', decoradorPermitirAE(views.updatePedidos), name='upd_pedidos'),

    #Marcas
    path('formuMarcas/', decoradorPermitirAE(views.formMarcas), name='form_marcas'),
    path('listarMarcas/', views.listarMarcas, name='list_marcas'),
    path('addMarcas/', decoradorPermitirAE(views.addMarcas), name='add_marcas'),
    path('elimMarcas/<int:id>', decoradorPermitirAE(views.deleteMarcas), name='del_marcas'),
    path('elimMarcas/', views.sinId, name='del_marcas_sin_id'),
    path('updateMarcasForm/<int:id>', decoradorPermitirAE(views.updateMarcasForm), name='upd_marcas_form'),
    path('updateMarcasForm/', views.sinId, name='upd_marcas_form_sin_id'),
    path('updateMarcas/', decoradorPermitirAE(views.updateMarcas), name='upd_marcas'),

    #Imagenes
    path('regImagenesForm/', views.regImagenesForm, name='reg_imagenes_form'),
    path('regImagenes/', views.regImagenes, name='reg_imagenes'),
    path('listImagenes/', views.listImagenes, name='list_imagenes'),


    #Compras
    path('verProductos/', views.verProductos, name='ver_prod'),

    #Inventario
    path('regInventario/', decoradorPermitirAE(views.registroInventario), name='reg_inv'),
    path('inventario/', decoradorPermitirAE(views.listarInventario), name='list_inv'),
    path('crearInv/', decoradorPermitirAE(views.crearInventario), name='crear_inv'),
    path('elimInv/<int:id>', decoradorPermitirAE(views.deleteInventario), name='del_inv'),
    path('elimInv/', views.sinId, name='del_inv_sin_id'),
    path('updateInvForm/<int:id>', decoradorPermitirAE(views.updateInventarioForm), name='upd_inv_form'),
    path('updateInvForm/', views.sinId, name='upd_inv_form_sin_id'),
    path('updateInv/', decoradorPermitirAE(views.updateInventario), name='upd_inv'),

    #PedidosProductos (inventario)
    path('formuPediProduc/', decoradorPermitirA(views.formPedidosProductos), name='form_pedidos_productos'),
    path('listarPediProduc/', decoradorPermitirA(views.listarPedidosProductos), name='list_pedidos_productos'),
    path('addPediProduc/', decoradorPermitirA(views.addPedidosProductos), name='add_pedidos_productos'),
    path('elimPediProduc/<id>', decoradorPermitirA(views.deletePedidosProductos), name='del_pedidos_productos'),
    path('elimPediProduc/', views.sinId, name='del_pedidos_productos_sin_id'),
    path('updatePediProducForm/<id>', decoradorPermitirA(views.updatePedidosProductosForm), name='upd_pedidos_productos_form'),
    path('updatePediProducForm/', views.sinId, name='upd_pedidos_productos_form_sin_id'),
    path('updatePediProduc/', decoradorPermitirA(views.updatePedidosProductos), name='upd_pedidos_productos'),

    #Ayuda
    path('ayuda/', views.ayuda, name='ayuda'),

    #Marcas
    path('marcas/', views.marcas, name='marcas'),

    #Carrito
    path('carritoCompras/', decoradorPermitirC(views.mostrarCarrito), name='carrito'),
    path('addCarrito/<int:id>', decoradorPermitirC(views.addCarrito), name='add_carrito'),
    path('vaciarCarrito/', decoradorPermitirC(views.vaciarCarrito), name='vaciar_carrito'),
    path('borrarElementoCarrito/<int:id>', decoradorPermitirC(views.borrarElementoCarrito), name='borrar_elemento_carrito'),


    #Admin - Roles
    path('listarRoles/', decoradorPermitirAE(views.listRoles), name='list_roles'),
    path('regRolesForm/', decoradorPermitirA(views.regRolesForm), name='reg_roles_form'),
    path('registroRoles/', decoradorPermitirA(views.rolRegistro), name='reg_roles'),
    path('deleteRoles/<int:id>', decoradorPermitirA(views.deleteRol), name='del_roles'),
    path('deleteRoles/', views.sinId, name='del_roles_sin_id'),
    path('updateRolesForm/<int:id>', decoradorPermitirA(views.updateRolForm), name='upd_roles_form'),
    path('updateRolesForm/', views.sinId, name='upd_roles_form_sin_id'),
    path('updateRoles/', decoradorPermitirA(views.updateRol), name='upd_roles'),


    #Envios
    path('listarEnvios/', decoradorPermitirAE(views.listEnvios), name='list_envios'),
    path('FormEnvios/', decoradorPermitirAE(views.formEnvios), name='form_envios'),
    path('addEnvios/', decoradorPermitirAE(views.addEnvios), name='add_envios'),
    path('deleteEnvios/<int:id>', decoradorPermitirAE(views.deleteEnvios), name='del_envios'),
    path('deleteEnvios/', views.sinId, name='del_envios_sin_id'),
    path('updateEnviosForm/<int:id>', decoradorPermitirAE(views.updateEnviosForm), name='upd_envios_form'),
    path('updateEnviosForm/', views.sinId, name='upd_envios_form_sin_id'),
    path('updateEnvios/', decoradorPermitirAE(views.updateEnvios), name='upd_envios'),
    

    #MediosDePago
    path('listarMediosPago/', decoradorPermitirA(views.listMediosPagos), name='list_mediosPagos'),
    path('formMediosPago/', decoradorPermitirA(views.formMediosPagos), name='form_mediosPagos'),
    path('addMedioPago/', decoradorPermitirA(views.addMediosPagos), name='add_medioPago'),
    path('deleteMedioPago/<int:id>', decoradorPermitirA(views.deleteMediosPagos), name='del_mediosPagos'),
    path('deleteMedioPago/', views.sinId, name='del_mediosPagos_sin_id'),
    path('updateMedioPagoForm/<int:id>', decoradorPermitirA(views.updateMediosPagosForm), name='upd_mediosPagos_form'),
    path('updateMedioPagoForm/', views.sinId, name='upd_mediosPagos_form_sin_id'),
    path('updateMedioPagos/', decoradorPermitirA(views.updateMediosPagos), name='upd_mediosPagos'),


    #Pagos
    path('listarPagos/', decoradorPermitirAE(views.listPagos), name='list_pagos'),
    path('formPagos/', decoradorPermitirA(views.formPagos), name='form_pagos'),
    path('addPagos/', decoradorPermitirA(views.addPagos), name='add_pagos'),
    path('deletePagos/<int:id>', decoradorPermitirA(views.deletePagos), name='del_pagos'),
    path('deletePagos/', views.sinId, name='del_pagos_sin_id'),
    path('updatePagosForm/<int:id>', decoradorPermitirA(views.updatePagosForm), name='upd_pagos_form'),
    path('updatePagosForm/', views.sinId, name='upd_pagos_form_sin_id'),
    path('updatePagos/', decoradorPermitirA(views.updatePagos), name='upd_pagos'),
]