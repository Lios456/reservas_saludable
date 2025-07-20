from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def index(request):
    return render(request, 'index.html')


# Views de Usuario

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/usuarios/')
        else:
            messages.error(request, 'Credenciales inválidas', extra_tags='danger')
    return render(request, 'login.html')

# Logout
@login_required(login_url='/login/')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/login/')



#Listar
@login_required(login_url='/login/')
@staff_member_required
def getallusuarios(request):
    usuarios = Usuario.objects.all()
    context = {'usuarios': usuarios}
    messages.success(request, 'Usuarios recuperados correctamente', extra_tags='success')
    return render(request, 'usuarios/list.html', context)

#Crear

#Editar

#Eliminar
@login_required(login_url='/login/')
@staff_member_required
def eliminarusuario(request, usuario_id):
    if request.method == 'POST':
        try:
            usuario = get_object_or_404(Usuario, id=usuario_id)
            usuario.delete()
            messages.success(request, 'Usuario eliminado correctamente', extra_tags='success')
        except Exception as e:
            messages.error(request, f'Error al eliminar el usuario: {str(e)}', extra_tags='error')
    else:
        messages.error(request, 'Método no permitido para esta operación', extra_tags='error')
    
    return redirect('/usuarios/')



# Views de Restaurante

#Listar

def getallrestaurantes(request):
    restaurantes = Restaurante.objects.all()
    context = {'restaurantes': restaurantes}
    return render(request, 'restaurantes/list.html', context)

#Crear

#Editar

#Eliminar
@login_required(login_url='/login/')
@staff_member_required
def eliminarrestaurante(request, restaurante_id):
    if request.method == 'POST':
        try:
            restaurante = get_object_or_404(Restaurante, id=restaurante_id)
            restaurante.delete()
            messages.success(request, 'Restaurante eliminado correctamente', extra_tags='success')
        except Exception as e:
            messages.error(request, f'Error al eliminar restaurante: {str(e)}', extra_tags='error')
    else:
        messages.error(request, 'Método no permitido', extra_tags='error')
    return redirect('/restaurantes/')



# Views de Menú

#Listar
def getallmenus(request):
    menus = Menu.objects.all()
    context = {'menus': menus}
    return render(request, 'menus/list.html', context)

#Crear

#Editar

#Eliminar
@login_required(login_url='/login/')
@staff_member_required
def eliminarmenu(request, menu_id):
    if request.method == 'POST':
        try:
            menu = get_object_or_404(Menu, id=menu_id)
            menu.delete()
            messages.success(request, 'Menú eliminado correctamente', extra_tags='success')
        except Exception as e:
            messages.error(request, f'Error al eliminar menú: {str(e)}', extra_tags='error')
    else:
        messages.error(request, 'Método no permitido', extra_tags='error')
    return redirect('/menus/')



# Views de Pedido

#Listar
def getallpedidos(request):
    pedidos = Pedido.objects.all()
    context = {'pedidos': pedidos}
    return render(request, 'pedidos/list.html', context)

#Crear

#Editar

#Eliminar
@login_required(login_url='/login/')
@staff_member_required
def eliminarpedido(request, pedido_id):
    if request.method == 'POST':
        try:
            pedido = get_object_or_404(Pedido, id=pedido_id)
            pedido.delete()
            messages.success(request, 'Pedido eliminado correctamente', extra_tags='success')
        except Exception as e:
            messages.error(request, f'Error al eliminar pedido: {str(e)}', extra_tags='error')
    else:
        messages.error(request, 'Método no permitido', extra_tags='error')
    return redirect('/pedidos/')



# Views de DetallesPedido

#Listar
def getalldetallespedido(request):
    detalles_pedido = DetallesPedido.objects.all()
    context = {'detalles_pedido': detalles_pedido}
    return render(request, 'detallespedido/list.html', context)

#Crear

#Editar

#Eliminar
@login_required(login_url='/login/')
@staff_member_required
def eliminardetallepedido(request, detalle_id):
    if request.method == 'POST':
        try:
            detalle = get_object_or_404(DetallePedido, id=detalle_id)
            detalle.delete()
            messages.success(request, 'Detalle de pedido eliminado correctamente', extra_tags='success')
        except Exception as e:
            messages.error(request, f'Error al eliminar detalle: {str(e)}', extra_tags='error')
    else:
        messages.error(request, 'Método no permitido', extra_tags='error')
    return redirect('/detallespedido/')



# Views de Repartidor

#Listar
def getallrepartidores(request):
    repartidores = Repartidor.objects.all()
    context = {'repartidores': repartidores}
    return render(request, 'repartidores/list.html', context)


#Crear

#Editar

#Eliminar
@login_required(login_url='/login/')
@staff_member_required
def eliminarrepartidor(request, repartidor_id):
    if request.method == 'POST':
        try:
            repartidor = get_object_or_404(Repartidor, id=repartidor_id)
            repartidor.delete()
            messages.success(request, 'Repartidor eliminado correctamente', extra_tags='success')
        except Exception as e:
            messages.error(request, f'Error al eliminar repartidor: {str(e)}', extra_tags='error')
    else:
        messages.error(request, 'Método no permitido', extra_tags='error')
    return redirect('/repartidores/')



# Views de Asignación de pedido

#Listar
def getallasignacionpedido(request):
    asignaciones_pedido = AsignacionPedido.objects.all()
    context = {'asignaciones_pedido': asignaciones_pedido}
    return render(request, 'asignacionpedido/list.html', context)

#Crear

#Editar

#Eliminar
@login_required(login_url='/login/')
@staff_member_required
def eliminarasignacion(request, asignacion_id):
    if request.method == 'POST':
        try:
            asignacion = get_object_or_404(AsignacionPedido, id=asignacion_id)
            asignacion.delete()
            messages.success(request, 'Asignación eliminada correctamente', extra_tags='success')
        except Exception as e:
            messages.error(request, f'Error al eliminar asignación: {str(e)}', extra_tags='error')
    else:
        messages.error(request, 'Método no permitido', extra_tags='error')
    return redirect('/asignacionpedido/')



