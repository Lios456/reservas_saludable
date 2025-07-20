from django.db import models

from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    dirección = models.CharField(max_length=255)
    teléfono = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Restaurante(models.Model):
    nombre = models.CharField(max_length=255)
    dirección = models.CharField(max_length=255)
    teléfono = models.CharField(max_length=20)
    horario = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Menu(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripción = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En preparación'),
        ('en_camino', 'En camino'),
        ('entregado', 'Entregado')
    ], default='pendiente')

    def __str__(self):
        return f'Pedido {self.id}'

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle {self.id}'

class Repartidor(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    teléfono = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class AsignacionPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    repartidor = models.ForeignKey(Repartidor, on_delete=models.CASCADE)

    def __str__(self):
        return f'Asignación {self.id}'