from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.index, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Usuarios
    path('usuarios/', views.getallusuarios, name='getallusuarios'),
    path('usuarios/crear/', views.crearusuario, name='crearusuario'),
    path('usuarios/editar/<int:usuario_id>/', views.editarusuario, name='editarusuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminarusuario, name='eliminarusuario'),

    # Restaurantes
    path('restaurantes/', views.getallrestaurantes, name='getallrestaurantes'),
    path('restaurantes/crear/', views.crearestaurante, name='crearestaurante'),
    path('restaurantes/editar/<int:restaurante_id>/', views.actualizarrestaurante, name='actualizarrestaurante'),
    path('restaurantes/eliminar/<int:restaurante_id>/', views.eliminarrestaurante, name='eliminarrestaurante'),

    # Menús
    path('menus/', views.getallmenus, name='getallmenus'),
    path('restaurantes/<int:id_restaurante>/menus/', views.getallmenusbyrestaurante, name='getallmenusbyrestaurante'),
    path('restaurantes/<int:id_restaurante>/menus/crear/', views.crearmenu, name='crearmenu'),
    path('menus/editar/<int:menu_id>/', views.actualizarmenu, name='actualizarmenu'),
    path('menus/eliminar/<int:menu_id>/', views.eliminarmenu, name='eliminarmenu'),

    # Pedidos
    path('pedidos/', views.getallpedidos, name='getallpedidos'),
    path('pedidos/crear/', views.crearpedido, name='crearpedido'),
    path('pedidos/editar/<int:pedido_id>/', views.actualizarpedido, name='actualizarpedido'),
    path('pedidos/eliminar/<int:pedido_id>/', views.eliminarpedido, name='eliminarpedido'),

    # Detalles de pedido
    path('detalles/', views.getalldetallespedido, name='getalldetallespedido'),
    path('detalles/crear/', views.creardetallespedido, name='creardetallespedido'),
    path('detalles/editar/<int:detalle_id>/', views.actualizardetallepedido, name='actualizardetallepedido'),
    path('detalles/eliminar/<int:detalle_id>/', views.eliminardetallepedido, name='eliminar_detallepedido'),

    # Repartidores
    path('repartidores/', views.getallrepartidores, name='getallrepartidores'),
    path('repartidores/crear/', views.crearrepartidor, name='crearrepartidor'),
    path('repartidores/editar/<int:repartidor_id>/', views.actualizarrepartidor, name='actualizarrepartidor'),
    path('repartidores/eliminar/<int:repartidor_id>/', views.eliminarrepartidor, name='eliminarrepartidor'),

    # Asignaciones
    path('asignaciones/', views.getallasignacionpedido, name='getallasignacionpedido'),
    path('repartidores/<int:id_repartidor>/asignaciones/', views.getallasignacionpedidobyrepartidor, name='getallasignacionpedidobyrepartidor'),
    path('pedidos/<int:id_pedido>/asignaciones/crear/', views.crearasignacion, name='crearasignacion'),
    path('asignaciones/editar/<int:asignacion_id>/', views.actualizarasignacion, name='actualizarasignacion'),
    path('asignaciones/eliminar/<int:asignacion_id>/', views.eliminarasignacion, name='eliminarasignacion'),

    # URLs del carrito - Versión HTML tradicional
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:menu_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:menu_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:menu_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/guardar/', views.guardar_carrito, name='guardar_carrito'),
]