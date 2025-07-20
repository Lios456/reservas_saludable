from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    #Usuario
    path('eliminarusuario/<int:usuario_id>/', views.eliminarusuario, name='eliminarusuario'),
    
    # Restaurante
    path('eliminarrestaurante/<int:restaurante_id>/', views.eliminarrestaurante, name='eliminarrestaurante'),
    
    #Menu
    path('eliminarmenu/<int:menu_id>/', views.eliminarmenu, name='eliminarmenu'),
    
    # Pedido
    path('eliminarpedido/<int:pedido_id>/', views.eliminarpedido, name='eliminarpedido'),
]