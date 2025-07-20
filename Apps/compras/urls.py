from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    #Usuario
    path('login/', views.login_view, name='login'),
    path('usuarios/', views.getallusuarios, name='getallusuarios'),
    path('eliminarusuario/<int:usuario_id>/', views.eliminarusuario, name='eliminarusuario'),
    
    # Restaurante
    path('restaurantes/', views.getallrestaurantes, name='getallrestaurantes'),
    path('eliminarrestaurante/<int:restaurante_id>/', views.eliminarrestaurante, name='eliminarrestaurante'),
    
    #Menu
    path('menus/', views.getallmenus, name='getallmenus'),
    path('eliminarmenu/<int:menu_id>/', views.eliminarmenu, name='eliminarmenu'),
    
    # Pedido
    path('pedidos/', views.getallpedidos, name='getallpedidos'),
    path('eliminarpedido/<int:pedido_id>/', views.eliminarpedido, name='eliminarpedido'),

    # Detalle Pedido
    path('detallespedido/', views.getalldetallespedido, name='getalldetallespedido'),
    path('eliminardetallespedido/<int:detallepedido_id>/', views.eliminardetallepedido, name='eliminardetallespedido'),

    # Repartidor
    path('repartidores/', views.getallrepartidores, name='getallrepartidores'),
    path('eliminarrepartidor/<int:repartidor_id>/', views.eliminarrepartidor, name='eliminarrepartidor'),

    # Asignaciones
    path('asignaciones/', views.getallasignacionpedido, name='getallasignaciones'),
    path('eliminarasignacion/', views.eliminarasignacion, name='eliminarasignacion')

]