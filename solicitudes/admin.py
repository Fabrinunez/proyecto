from django.contrib import admin
from django.contrib import admin
from .models import Producto, Pedido


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)
    ordering = ('categoria', 'nombre')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'estado', 'fecha_evento', 'total')
    list_filter = ('estado', 'fecha_evento')
    search_fields = ('cliente_nombre',)
    ordering = ('fecha_evento',)

