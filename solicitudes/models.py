from django.db import models

# Create your models here.
from django.db import models

# -----------------------------
#   MODELO: PRODUCTO / SERVICIO
# -----------------------------
class Producto(models.Model):
    CATEGORIAS = [
        ('INMOBILIARIO', 'Inmobiliario (mesas, sillas, mantelería, vajilla)'),
        ('BANQUETE', 'Banquete (alimentos, bebidas, degustación)'),
        ('MUSICA', 'Música / DJ'),
        ('ILUMINACION', 'Iluminación'),
        ('DECORACION', 'Decoración'),
        ('COORDINACION', 'Coordinación del evento'),
    ]

    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"


# -----------------------------
#   MODELO: RESERVA / PEDIDO
# -----------------------------
class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente_nombre = models.CharField(max_length=120)
    cliente_email = models.EmailField()
    fecha_evento = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    # Relación con productos/servicios del evento
    productos = models.ManyToManyField(Producto, related_name='pedidos')

    # Total calculado automáticamente
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def calcular_total(self):
        """Suma los precios de todos los productos asociados."""
        return sum(producto.precio for producto in self.productos.all())

    def save(self, *args, **kwargs):
        """Actualiza el total antes de guardar."""
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente_nombre} ({self.estado})"