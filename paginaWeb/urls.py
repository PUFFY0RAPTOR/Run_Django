from django.urls import path
from . import views
from .views import decoradorPermitirAE, decoradorDenegarAEC, decoradorPermitirAEC, decoradorPermitirA, \
    decoradorPermitirC, decoradorPermitirAC, decoradorPermitirAV

app_name = "paginaWeb"
urlpatterns = [
    path('', views.index, name='index'),

    # Login
    path('loginForm/', decoradorDenegarAEC(views.loginForm), name='login_form'),
    path('login/', decoradorDenegarAEC(views.login), name='login'),
    path('logout/', decoradorPermitirAEC(views.logout), name='logout'),

    # Nuevo código
    # path('personasForm/', views.registrarPersonasForm, name='personas_form'),
    # path('registrarPersonas/', views.registrarPersonas, name='reg_personas'),

    # perfil
    path('perfil/', views.perfil, name='perfil'),

    path('registroPersona/', decoradorPermitirAV(views.registro), name='registro'),
    path('guardarPersona/', decoradorPermitirAEC(views.guardarPersona), name='guardarPersona'),
    path('eliminarPersona/<int:id>', decoradorPermitirAC(views.eliminarPersona), name='delPersona'),
    path('eliminarPersona/', views.sinId, name='del_persona_sin_id'),
    path('personaEditar/<int:id>', decoradorPermitirAEC(views.buscarPersonaEditar), name="upd_personas_form"),
    path('personaEditar/', views.sinId, name='upd_persona_sin_id'),
    path('updatePersona/', decoradorPermitirAEC(views.updatePersona), name='updPersona'),
    path('listarPersonas/', decoradorPermitirAE(views.listarPersonas), name='list_usu'),

    # Empleados
    # path('formuEmpleados/', decoradorPermitirA(views.formEmpleados), name='form_empleados'),
    # path('listarEmpleados/', decoradorPermitirA(views.listarEmpleados), name='list_empleados'),
    # path('addEmpleados/', decoradorPermitirA(views.addEmpleados), name='add_empleados'),
    # path('elimEmpleados/<id>', decoradorPermitirA(views.deleteEmpleados), name='del_empleados'),
    # path('elimEmpleados/', views.sinId, name='del_empleados_sin_id'),
    # path('updateEmpleadosForm/<id>', decoradorPermitirA(views.updateEmpleadosForm), name='upd_empleados_form'),
    # path('updateEmpleadosForm/', views.sinId, name='upd_empleados_form_sin_id'),
    # path('updateEmpleados/', decoradorPermitirA(views.updateEmpleados), name='upd_empleados'),

    # Usuarios
    path('formuUsuarios/', decoradorPermitirA(views.formUsuarios), name='form_usuarios'),
    path('listarUsuarios/', decoradorPermitirA(views.listarUsuarios), name='list_usuarios'),
    path('addUsuarios/', decoradorPermitirA(views.addUsuarios), name='add_usuarios'),
    path('elimUsuarios/<id>', decoradorPermitirA(views.deleteUsuarios), name='del_usuarios'),
    path('elimUsuarios/', views.sinId, name='del_usuarios_sin_id'),
    path('updateUsuariosForm/<id>', decoradorPermitirA(views.updateUsuariosForm), name='upd_usuarios_form'),
    path('updateUsuariosForm/', views.sinId, name='upd_usuarios_form_sin_id'),
    path('updateUsuarios/', decoradorPermitirA(views.updateUsuarios), name='upd_usuarios'),

    # Ventas
    path('formuVentas/', decoradorPermitirAE(views.formVentas), name='form_ventas'),
    path('listarVentas/', decoradorPermitirAE(views.listarVentas), name='list_ventas'),
    path('addVentas/', decoradorPermitirAE(views.addVentas), name='add_ventas'),
    path('elimVentas/<id>', decoradorPermitirAE(views.deleteVentas), name='del_ventas'),
    path('elimVentas/', views.sinId, name='del_ventas_sin_id'),
    path('updateVentasForm/<id>', decoradorPermitirAE(views.updateVentasForm), name='upd_ventas_form'),
    path('updateVentasForm/', views.sinId, name='upd_ventas_form_sin_id'),
    path('updateVentas/', decoradorPermitirAE(views.updateVentas), name='upd_ventas'),



    # Marcas
    path('formuMarcas/', decoradorPermitirAE(views.formMarcas), name='form_marcas'),
    path('listarMarcas/', views.listarMarcas, name='list_marcas'),
    path('addMarcas/', decoradorPermitirAE(views.addMarcas), name='add_marcas'),
    path('elimMarcas/<int:id>', decoradorPermitirAE(views.deleteMarcas), name='del_marcas'),
    path('elimMarcas/', views.sinId, name='del_marcas_sin_id'),
    path('updateMarcasForm/<int:id>', decoradorPermitirAE(views.updateMarcasForm), name='upd_marcas_form'),
    path('updateMarcasForm/', views.sinId, name='upd_marcas_form_sin_id'),
    path('updateMarcas/', decoradorPermitirAE(views.updateMarcas), name='upd_marcas'),

    # Categorias
    path('formuCate/', decoradorPermitirAE(views.formCategorias), name='form_categorias'),
    path('listarCategorias/', views.listarCategorias, name='list_categorias'),
    path('addCategorias/', decoradorPermitirAE(views.addCategorias), name='add_categorias'),
    path('elimCategorias/<int:id>', decoradorPermitirAE(views.deleteCategorias), name='del_categorias'),
    path('elimCategorias/', views.sinId, name='del_categorias_sin_id'),
    path('updateCategoriasForm/<int:id>', decoradorPermitirAE(views.updateCategoriasForm), name='upd_categorias_form'),
    path('updateCategoriasForm/', views.sinId, name='upd_categorias_form_sin_id'),
    path('updateCategoria/', decoradorPermitirAE(views.updateCategorias), name='upd_categorias'),


    # Imagenes
    path('regImagenesForm/', views.regImagenesForm, name='reg_imagenes_form'),
    path('regImagenes/', views.regImagenes, name='reg_imagenes'),
    path('listImagenes/', views.listImagenes, name='list_imagenes'),

    # Compras
    path('verProductos/', views.verProductos, name='ver_prod'),

    # Inventario
    path('regInventario/', decoradorPermitirAE(views.registroInventario), name='reg_inv'),
    path('inventario/', decoradorPermitirAE(views.listarInventario), name='list_inv'),
    path('crearInv/', decoradorPermitirAE(views.crearInventario), name='crear_inv'),
    path('elimInv/<int:id>', decoradorPermitirAE(views.deleteInventario), name='del_inv'),
    path('elimInv/', views.sinId, name='del_inv_sin_id'),
    path('updateInvForm/<int:id>', decoradorPermitirAE(views.updateInventarioForm), name='upd_inv_form'),
    path('updateInvForm/', views.sinId, name='upd_inv_form_sin_id'),
    path('updateInv/', decoradorPermitirAE(views.updateInventario), name='upd_inv'),

    # Pedidos
    path('formuPedi/', decoradorPermitirA(views.formPedidos), name='form_pedidos'),
    path('listarPedi/', decoradorPermitirA(views.listarPedidos), name='list_pedidos'),
    path('addPedi/', decoradorPermitirA(views.addPedidos), name='add_pedidos'),
    path('elimPedi/<id>', decoradorPermitirA(views.deletePedidos), name='del_pedidos'),
    path('elimPedi/', views.sinId, name='del_pedidos_sin_id'),
    path('updatePediForm/<id>', decoradorPermitirA(views.updatePedidosForm),
         name='upd_pedidos_productos_form'),
    path('updatePediProducForm/', views.sinId, name='upd_pedidos_productos_form_sin_id'),
    path('updatePediProduc/', decoradorPermitirA(views.updatePedidosProductos), name='upd_pedidos_productos'),

    # Ayuda
    path('ayuda/', views.ayuda, name='ayuda'),

    # Marcas
    path('marcas/', views.marcas, name='marcas'),

    # Carrito
    path('carritoCompras/', decoradorPermitirC(views.mostrarCarrito), name='carrito'),
    path('addCarrito/<int:id>', decoradorPermitirC(views.addCarrito), name='add_carrito'),
    path('vaciarCarrito/', decoradorPermitirC(views.vaciarCarrito), name='vaciar_carrito'),
    path('borrarElementoCarrito/<int:id>', decoradorPermitirC(views.borrarElementoCarrito),
         name='borrar_elemento_carrito'),

    # Admin - Roles
    path('listarRoles/', decoradorPermitirAE(views.listRoles), name='list_roles'),
    path('regRolesForm/', decoradorPermitirA(views.regRolesForm), name='reg_roles_form'),
    path('registroRoles/', decoradorPermitirA(views.rolRegistro), name='reg_roles'),
    path('deleteRoles/<int:id>', decoradorPermitirA(views.deleteRol), name='del_roles'),
    path('deleteRoles/', views.sinId, name='del_roles_sin_id'),
    path('updateRolesForm/<int:id>', decoradorPermitirA(views.updateRolForm), name='upd_roles_form'),
    path('updateRolesForm/', views.sinId, name='upd_roles_form_sin_id'),
    path('updateRoles/', decoradorPermitirA(views.updateRol), name='upd_roles'),


    # MediosDePago
    path('listarMediosPago/', decoradorPermitirA(views.listMediosPagos), name='list_mediosPagos'),
    path('formMediosPago/', decoradorPermitirA(views.formMediosPagos), name='form_mediosPagos'),
    path('addMedioPago/', decoradorPermitirA(views.addMediosPagos), name='add_medioPago'),
    path('deleteMedioPago/<int:id>', decoradorPermitirA(views.deleteMediosPagos), name='del_mediosPagos'),
    path('deleteMedioPago/', views.sinId, name='del_mediosPagos_sin_id'),
    path('updateMedioPagoForm/<int:id>', decoradorPermitirA(views.updateMediosPagosForm), name='upd_mediosPagos_form'),
    path('updateMedioPagoForm/', views.sinId, name='upd_mediosPagos_form_sin_id'),
    path('updateMedioPagos/', decoradorPermitirA(views.updateMediosPagos), name='upd_mediosPagos'),

    # Pagos
    path('listarPagos/', decoradorPermitirAE(views.listPagos), name='list_pagos'),
    path('formPagos/', decoradorPermitirA(views.formPagos), name='form_pagos'),
    path('addPagos/', decoradorPermitirA(views.addPagos), name='add_pagos'),
    path('deletePagos/<int:id>', decoradorPermitirA(views.deletePagos), name='del_pagos'),
    path('deletePagos/', views.sinId, name='del_pagos_sin_id'),
    path('updatePagosForm/<int:id>', decoradorPermitirA(views.updatePagosForm), name='upd_pagos_form'),
    path('updatePagosForm/', views.sinId, name='upd_pagos_form_sin_id'),
    path('updatePagos/', decoradorPermitirA(views.updatePagos), name='upd_pagos'),
]
