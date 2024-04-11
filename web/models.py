from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Producto (models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos', blank=True)

    def __str__(self):
        return self.nombre

# relacion 1 a 1 con la tabla User de django


class Cientes (models.Model):
    usuario = models.OneToOneField(User, on_delete=models.RESTRICT)
    cedula = models.CharField(max_length=13)
    sexo = models.CharField(max_length=1, default='M')
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username + " - " + self.cedula


class Pedido(models.Model):

    ESTADO_CHOICES = (
        ('P', 'Pendiente'),
        ('E', 'Enviado'),
        ('C', 'Pagado'),
    )

    # relacion con la tabla clientes (1 a muchos) es decir un cliente puede tener muchos pedidos
    # ForeignKey = llave foranea (relacion 1 a muchos)
    cliente = models.ForeignKey(Cientes, on_delete=models.RESTRICT)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    nro_pedido = models.CharField(max_length=20, null=True)
    fecha_entrega = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(
        max_length=1, default='P', choices=ESTADO_CHOICES)

    def __str__(self):
        return self.cliente.usuario.username + " - " + str(self.fecha_pedido)


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.producto.nombre + " - " + str(self.cantidad)
