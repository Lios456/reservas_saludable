from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    #Usuario
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('usuarios/', views.getallusuarios, name='getallusuarios'),
    path('crearusuario/', views.crearusuario, name='crearusuario'),
    path('editarusuario/<int:usuario_id>/', views.editarusuario, name='editarusuario'),
    path('eliminarusuario/<int:usuario_id>/', views.eliminarusuario, name='eliminarusuario'),
    
    # Restaurante
    path('restaurantes/', views.getallrestaurantes, name='getallrestaurantes'),
    path('crearestaurante/', views.crearestaurante, name='crearestaurante'),
    path('actualizarrestaurante/<int:restaurante_id>/', views.actualizarrestaurante, name='actualizarrestaurante'),
    path('eliminarrestaurante/<int:restaurante_id>/', views.eliminarrestaurante, name='eliminarrestaurante'),
    
    #Menu
    path('menus/', views.getallmenus, name='getallmenus'),
    path('menus/<int:id_restaurante>/', views.getallmenusbyrestaurante, name='getallmenusbyrestaurante'),
    path('crearmenu/<int:id_restaurante>/', views.crearmenu, name='crearmenu'),
    path('actualizarmenu/<int:menu_id>/', views.actualizarmenu, name='actualizarmenu'),
    path('eliminarmenu/<int:menu_id>/', views.eliminarmenu, name='eliminarmenu'),
    
    # Pedido
    path('pedidos/', views.getallpedidos, name='getallpedidos'),
    path('crearpedido/', views.crearpedido, name='crearpedido'),
    path('actualizarpedido/<int:pedido_id>/', views.actualizarpedido, name='actualizarpedido'),
    path('eliminarpedido/<int:pedido_id>/', views.eliminarpedido, name='eliminarpedido'),

    # Detalle Pedido
    path('detallespedido/', views.getalldetallespedido, name='getalldetallespedido'),
    path('creardetallespedido/', views.creardetallespedido, name='creardetallespedido'),
    path('actualizardetallespedido/<int:detallepedido_id>/', views.actualizardetallepedido, name='actualizardetallespedido'),
    path('eliminardetallespedido/<int:detallepedido_id>/', views.eliminardetallepedido, name='eliminardetallespedido'),

    # Repartidor
    path('repartidores/', views.getallrepartidores, name='getallrepartidores'),
    path('crearrepartidor/', views.crearrepartidor, name='crearrepartidor'),
    path('actualizarrepartidor/<int:repartidor_id>/', views.actualizarrepartidor, name='actualizarrepartidor'),
    path('eliminarrepartidor/<int:repartidor_id>/', views.eliminarrepartidor, name='eliminarrepartidor'),

    # Asignaciones
    path('asignaciones/', views.getallasignacionpedido, name='getallasignaciones'),
    path('asignaciones/<int:id_repartidor>/', views.getallasignacionpedidobyrepartidor, name='getallasignacionpedidobyrepartidor'),
    path('crearasignacion/<int:id_pedido>/', views.crearasignacion, name='crearasignacion'),
    path('actualizarasignacion/<int:asignacion_id>/', views.actualizarasignacion, name='actualizarasignacion'),
    path('eliminarasignacion/', views.eliminarasignacion, name='eliminarasignacion'),

    #Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

]