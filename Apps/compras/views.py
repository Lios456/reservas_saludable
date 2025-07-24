from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import User, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import  *
from django.db.models import Count, Sum, F



# Create your views here.

# ============================================================================================================
# Dashboard
# ============================================================================================================

def dashboard(request):

    #============
    # KPI 1 Total usuarios registrados
    #============

    total_usuarios = User.objects.count()


    #============
    # KPI 2 Total de restaurantes registrados
    #============
    total_restaurantes = Restaurante.objects.count()

    #============
    # KPI 3 Total de pedidos
    #============
    total_pedidos = Pedido.objects.count()

    #============
    # KPI 4 Total de pedidos entregados
    #============
    total_pedidos_entregados = Pedido.objects.filter(estado='entregado').count()

    #============
    # KPI 5 Total pedidos pendientes
    #============
    total_pedidos_pendientes =Pedido.objects.filter(estado='pendiente').count()


    #============
    # KPI 6 Total de pedidos en camino
    #============
    total_pedidos_en_camino =Pedido.objects.filter(estado='en_camino').count()

    #============
    # KPI 7 Total de pedidos en preparación
    #============
    total_pedidos_en_preparacion =Pedido.objects.filter(estado='en_preparacion').count()

    #============
    # KPI 8 Porcentaje de pedidos en preparación
    porcentaje_pedidos_en_preparacion = (total_pedidos_en_preparacion / Pedido.objects.count()) * 100 if Pedido.objects.count() > 0 else 0
    #============


    #============
    # KPI 9 Ingresos totales
    #============
    ingresos_totales = sum(p.total for p in Pedido.objects.filter(estado='entregado'))


    #============
    # KPI 10 Repartidores con más entregas
    #============
    repartidores_con_mas_entregas = Repartidor.objects.annotate(total_entregas=Count('asignacionpedido__pedido')).order_by('-total_entregas')[:10]

    #============
    # KPI 11 5 Platos más vendidos
    #============
    platos_mas_vendidos = DetallePedido.objects.values('menu__nombre').annotate(total=Sum('cantidad')).order_by('-total')[:5]
    
    #============
    # KPI 12 5 Restaurantes con más pedidos
    #============
    pedidos_por_restaurante = Pedido.objects.values('restaurante__nombre').annotate(total=Count('id')).order_by('-total')[:5]

    #===========
    # KPI 13 3 Usuarios con más pedidos
    #===========
    pedidos_por_usuario = Pedido.objects.values('usuario__username').annotate(total=Count('id')).order_by('-total')[:3]


    #===========
    # CONTEXTO
    #===========

    context = {
        'total_pedidos': total_pedidos,
        'total_pedidos_entregados': total_pedidos_entregados,
        'total_pedidos_pendientes': total_pedidos_pendientes,
        'total_usuarios': total_usuarios,
        'total_restaurantes': total_restaurantes,
        'total_pedidos_en_camino': total_pedidos_en_camino,
        'total_pedidos_en_preparacion':total_pedidos_en_preparacion,
        'ingresos_totales': ingresos_totales,
        'repartidores_con_mas_entregas': repartidores_con_mas_entregas,
        'platos_mas_vendidos': platos_mas_vendidos,
        'pedidos_por_restaurante':pedidos_por_restaurante,
        'pedidos_por_usuario':pedidos_por_usuario

    }


    return render(request, 'dashboard.html', context)

def index(request):
    return render(request, 'index.html')

# ============================================================================================================
# Views de Usuario
# ============================================================================================================

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/usuarios/')
            else:
                return redirect('/restaurantes/')
        else:
            messages.error(request, 'Credenciales inválidas', extra_tags='danger')
    return render(request, 'auth/login.html')

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
    usuarios = User.objects.all()
    context = {'usuarios': usuarios}
    messages.success(request, 'Usuarios recuperados correctamente', extra_tags='success')
    return render(request, 'usuarios/list.html', context)

#Crear
def crearusuario(request):
    if request.method == 'POST':
        usuario = User()
        usuario.username = request.POST.get('username', '').strip()
        usuario.email = request.POST.get('email', '').strip()
        usuario.set_password(request.POST.get('password', '').strip())
        usuario.is_staff = False
        usuario.save()
        messages.success(request, 'Usuario creado correctamente', extra_tags='success')
        return redirect('/usuarios/')
    else:
        return render(request, 'usuarios/form.html')


#Editar
@login_required(login_url='/login/')
def editarusuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    if request.method == 'POST':
        usuario.username = request.POST.get('username') or usuario.username
        usuario.email = request.POST.get('email') or usuario.email
        usuario.set_password(request.POST.get('password', '').strip() or usuario.password)
        usuario.save()
        messages.success(request, 'Usuario editado correctamente', extra_tags='success')
        return redirect('/usuarios/')
    else:
        form = UserCreationForm(instance=usuario)
        return render(request, 'usuarios/form.html', {'usuario':usuario})


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


# ============================================================================================================
# Views de Restaurante
# ============================================================================================================

#Listar

def getallrestaurantes(request):
    restaurantes = Restaurante.objects.all()
    context = {'restaurantes': restaurantes}
    return render(request, 'restaurantes/list.html', context)

#Crear
@login_required(login_url='/login/')
@staff_member_required
def crearestaurante(request):
    if request.method == 'POST':
        restaurante = Restaurante()
        restaurante.nombre = request.POST.get('nombre', '').strip()
        restaurante.direccion = request.POST.get('direccion', '').strip()
        restaurante.telefono = request.POST.get('telefono', '').strip()
        restaurante.horario = request.POST.get('horario', '').strip()
        restaurante.save()
        messages.success(request, 'Restaurante creado exitosamente.')
        return redirect('/restaurantes/')
            
    else:
        return render(request, 'restaurantes/form.html')


#Editar

@login_required(login_url='/login/')
@staff_member_required
def actualizarrestaurante(request, restaurante_id):
    restaurante = Restaurante.objects.get(pk=restaurante_id)
    if request.method == 'POST':
        restaurante.nombre = request.POST.get('nombre', '').strip()
        restaurante.direccion = request.POST.get('direccion', '').strip()
        restaurante.telefono = request.POST.get('telefono', '').strip()
        restaurante.horario = request.POST.get('horario', '').strip()
        restaurante.save()
        messages.success(request, 'Restaurante editado exitosamente.')
        return redirect('/restaurantes/')
            
    else:
        return render(request, 'restaurantes/form.html', {'restaurante': restaurante})

#Eliminar
@login_required(login_url='/login/')
@staff_member_required
def eliminarrestaurante(request, restaurante_id):
    if request.method == 'POST':
        try:
            restaurante = get_object_or_404(Restaurante, pk=restaurante_id)
            restaurante.delete()
            messages.success(request, 'Restaurante eliminado correctamente', extra_tags='success')
        except Exception as e:
            messages.error(request, f'Error al eliminar restaurante: {str(e)}', extra_tags='error')
    else:
        messages.error(request, 'Método no permitido', extra_tags='error')
    return redirect('/restaurantes/')



# ============================================================================================================
# Views de Menú
# ============================================================================================================

#Listar
def getallmenus(request):
    menus = Menu.objects.all()
    context = {'menus': menus}
    return render(request, 'menus/list.html', context)

def getallmenusbyrestaurante(request, id_restaurante):
    menus = Menu.objects.filter(restaurante_id=id_restaurante)
    context = {'menus': menus, 'restaurante': Restaurante.objects.get(pk=id_restaurante)}
    return render(request,'menus/list.html', context)
#Crear
@login_required(login_url='/login/')
@staff_member_required
def crearmenu(request, id_restaurante):
    restaurante = Restaurante.objects.get(pk=id_restaurante)
    if request.method == 'POST':
        menu = Menu()
        menu.nombre = request.POST.get('nombre', '').strip()
        menu.descripcion = request.POST.get('descripcion', '').strip()
        menu.precio = request.POST.get('precio', '').strip()
        menu.restaurante = restaurante
        menu.foto = request.FILES.get('foto')
        menu.save()
        messages.success(request, 'Menú creado exitosamente.')
        return redirect(f'/menus/{restaurante.id}')
    else:
        context = {'restaurante': restaurante}
        return render(request, 'menus/form.html', context)

#Editar
@login_required(login_url='/login/')
@staff_member_required
def actualizarmenu(request, menu_id):
    menu = Menu.objects.get(pk=menu_id)
    if request.method == 'POST':
        menu.nombre = request.POST.get('nombre', '').strip()
        menu.descripcion = request.POST.get('descripcion', '').strip()
        menu.precio = request.POST.get('precio', '').strip()
        menu.foto = request.FILES.get('foto') or menu.foto
        menu.save()
        messages.success(request, 'Menú actualizado exitosamente.')
        return redirect('/restaurantes/')
    else:
        return render(request, 'menus/form.html', {'menu': menu})

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
    return redirect('/restaurantes/')


# ============================================================================================================
# Views de Pedido
# ============================================================================================================

#Listar
@login_required(login_url='/login/')
def getallpedidos(request):
    if(request.user.is_staff):
        pedidos = Pedido.objects.all()
    else:
        pedidos = Pedido.objects.filter(usuario=request.user)
    context = {'pedidos': pedidos}
    return render(request, 'pedidos/list.html', context)

#Crear
@login_required(login_url='/login/')
def crearpedido(request):
    if request.method == 'POST':
        pedido = Pedido()
        pedido.fecha = request.POST.get('fecha')
        pedido.estado = request.POST.get('estado', '').strip()
        pedido.total = request.POST.get('total')
        pedido.usuario_id = request.user.id
        pedido.save()
        messages.success(request, 'Pedido creado exitosamente.')
        return redirect('/pedidos/')
    else:
        return render(request, 'pedidos/form.html')

#Editar
@login_required(login_url='/login/')
def actualizarpedido(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    if request.method == 'POST':
        pedido.fecha = request.POST.get('fecha')
        pedido.estado = request.POST.get('estado', '').strip()
        pedido.total = request.POST.get('total')
        pedido.save()
        messages.success(request, 'Pedido actualizado exitosamente.')
        return redirect('/pedidos/')
    else:
        return render(request, 'pedidos/form.html', {'pedido': pedido})

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


# ============================================================================================================
# Views de DetallesPedido
# ============================================================================================================

#Listar
def getalldetallespedido(request):
    detalles_pedido = DetallesPedido.objects.all()
    context = {'detalles_pedido': detalles_pedido}
    return render(request, 'detalles/list.html', context)

carrito = []
#Crear
@login_required(login_url='/login/')
def creardetallespedido(request):
    if request.method == 'POST':
        # Creo el detalle
        detalle = DetallesPedido()
        detalle.cantidad = request.POST.get('cantidad')
        detalle.subtotal = request.POST.get('subtotal')
        detalle.pedido_id = request.POST.get('pedido_id')
        detalle.menu_id = request.POST.get('menu_id')
        # Lo agrego a la lista
        carrito.append(detalle)
        messages.success(request, 'Detalle de pedido creado exitosamente.')
        return redirect('/detallespedido/')
    else:
        return render(request, 'detalles/form.html')

#Guardar
@login_required(login_url='/login/')
def guardardetalles(request):
    if request.method == 'POST':
        #Verifico si el carrito tiene por lo menos un detalle
        if len(carrito) >=1:
            for detalle in carrito:
                detalle.save()
            messages.success(request, 'Detalles guardados exitosamente.')
            return redirect('/detallespedido/')
        else:
            messages.error(request, 'No tienes agregado ningún menú')
            return redirect('/pedidos/')


#Editar
@login_required(login_url='/login/')
def actualizardetallepedido(request, detalle_id):
    detalle = DetallesPedido.objects.get(pk=detalle_id)
    if request.method == 'POST':
        detalle.cantidad = request.POST.get('cantidad')
        detalle.subtotal = request.POST.get('subtotal')
        detalle.pedido_id = request.POST.get('pedido_id')
        detalle.menu_id = request.POST.get('menu_id')
        detalle.save()
        messages.success(request, 'Detalle de pedido actualizado exitosamente.')
        return redirect('/detallespedido/')
    else:
        return render(request, 'detalles/form.html', {'detalle': detalle})

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


# ============================================================================================================
# Views de Repartidor
# ============================================================================================================

#Listar
def getallrepartidores(request):
    repartidores = Repartidor.objects.all()
    context = {'repartidores': repartidores}
    return render(request, 'repartidores/list.html', context)


#Crear
@login_required(login_url='/login/')
@staff_member_required
def crearrepartidor(request):
    if request.method == 'POST':
        repartidor = Repartidor()
        repartidor.nombre = request.POST.get('nombre', '').strip()
        repartidor.apellido = request.POST.get('apellido', '').strip()
        repartidor.direccion = request.POST.get('direccion', '').strip()
        repartidor.edad = request.POST.get('edad', '').strip()
        repartidor.telefono = request.POST.get('telefono', '').strip()
        repartidor.save()
        messages.success(request, 'Repartidor creado exitosamente.')
        return redirect('/repartidores/')
    else:
        return render(request, 'repartidores/form.html')

#Editar
@login_required(login_url='/login/')
@staff_member_required
def actualizarrepartidor(request, repartidor_id):
    repartidor = Repartidor.objects.get(pk=repartidor_id)
    if request.method == 'POST':
        repartidor.nombre = request.POST.get('nombre', '').strip()
        repartidor.apellido = request.POST.get('apellido', '').strip()
        repartidor.edad = request.POST.get('edad', '').strip()
        repartidor.telefono = request.POST.get('telefono', '').strip()
        repartidor.direccion = request.POST.get('direccion', '').strip()
        repartidor.save()
        messages.success(request, 'Repartidor actualizado exitosamente.')
        return redirect('/repartidores/')
    else:
        return render(request, 'repartidores/form.html', {'repartidor': repartidor})

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


# ============================================================================================================
# Views de Asignación de pedido
# ============================================================================================================

#Listar
def getallasignacionpedido(request):
    asignaciones_pedido = AsignacionPedido.objects.all()
    context = {'asignaciones_pedido': asignaciones_pedido}
    return render(request, 'asignaciones/list.html', context)

def getallasignacionpedidobyrepartidor(request, id_repartidor):
    asignaciones_pedido = AsignacionPedido.objects.filter(repartidor_id=id_repartidor)
    context = {'asignaciones_pedido': asignaciones_pedido, 'id_repartidor': id_repartidor}
    return render(request, 'asignaciones/list.html', context)
#Crear
@login_required(login_url='/login/')
@staff_member_required
def crearasignacion(request, id_pedido):
    pedido = Pedido.objects.get(pk=id_pedido)
    if request.method == 'POST':
        #Ver si ese pedido ya tiene asignación
        if AsignacionPedido.objects.filter(pedido_id=id_pedido).exists():
            messages.error(request, 'Este pedido ya tiene asignación', extra_tags='danger')
            return redirect('/pedidos/')
        #Ver si el pedido está en estado "En camino"
        if pedido.estado == 'en_camino':
            messages.error(request, 'Este pedido no puede ser asignado porque está en estado "En camino"', extra_tags='danger')
            return redirect('/pedidos/')
        #Ver si el pedido está en estado "Entregado"
        if pedido.estado == 'entregado':
            messages.error(request, 'Este pedido no puede ser asignado porque está en estado "Entregado"', extra_tags='danger')
            return redirect('/pedidos/')
        
        asignacion = AsignacionPedido()
        asignacion.fecha_asignacion = request.POST.get('fecha_asignacion')
        asignacion.estado = request.POST.get('estado', '').strip()
        asignacion.pedido_id = request.POST.get('pedido_id')
        asignacion.repartidor_id = request.POST.get('repartidor_id')
        asignacion.save()
        messages.success(request, 'Asignación creada exitosamente.')
        return redirect('/pedidos/')
    else:
        context = {
            'pedido': pedido,
            'repartidores': Repartidor.objects.all()
        }
        return render(request, 'asignaciones/form.html', context)

#Editar
@login_required(login_url='/login/')
@staff_member_required
def actualizarasignacion(request, asignacion_id):
    asignacion = AsignacionPedido.objects.get(pk=asignacion_id)
    if request.method == 'POST':
        asignacion.fecha_asignacion = request.POST.get('fecha_asignacion')
        asignacion.estado = request.POST.get('estado', '').strip()
        asignacion.pedido_id = request.POST.get('pedido_id')
        asignacion.repartidor_id = request.POST.get('repartidor_id')
        asignacion.save()
        messages.success(request, 'Asignación actualizada exitosamente.')
        return redirect('/asignacionpedido/')
    else:
        return render(request, 'asignaciones/form.html', {'asignacion': asignacion})

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



