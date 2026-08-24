from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response

from solicitudes.dao.ReVenuedao import ProductoDAO, PedidoDAO
from solicitudes.serializers import ProductoSerializer, PedidoSerializer


# ==========================================
# 1. VISTAS WEB (HTML)
# ==========================================

def home_view(request):
    """Página principal del sistema"""
    return render(request, 'mainvista/home.html')


def catalogo_view(request):
    """Muestra el catálogo de servicios y mobiliario"""
    productos = ProductoDAO.obtener_disponibles()
    return render(request, 'mainvista/catalogo.html', {'productos': productos})


def reservas_view(request):
    """Vista administrativa: muestra todas las reservas activas"""
    pedidos = PedidoDAO.obtener_todos()
    return render(request, 'mainvista/reservas.html', {'pedidos': pedidos})


def crear_reserva_action(request):
    """Procesa el formulario web para crear una nueva reserva"""
    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente_nombre')
        cliente_email = request.POST.get('cliente_email')
        fecha_evento = request.POST.get('fecha_evento')
        productos_ids = request.POST.getlist('productos_ids')

        PedidoDAO.crear_reserva(
            cliente_nombre=cliente_nombre,
            cliente_email=cliente_email,
            fecha_evento=fecha_evento,
            productos_ids=productos_ids
        )

        return redirect('reservas')

    # Si es GET, mostrar formulario
    productos = ProductoDAO.obtener_disponibles()
    return render(request, 'mainvista/crear_reserva.html', {'productos': productos})


def cambiar_estado_action(request, pedido_id):
    """Actualiza el estado de una reserva desde la vista web"""
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        PedidoDAO.cambiar_estado(pedido_id, nuevo_estado)
    return redirect('reservas')


# ==========================================
# 2. API REST (JSON)
# ==========================================

class ProductoViewSet(viewsets.ViewSet):
    """API REST para productos/servicios"""
    def list(self, request):
        productos = ProductoDAO.obtener_todos()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)


class PedidoViewSet(viewsets.ViewSet):
    """API REST para reservas de eventos"""
    def list(self, request):
        pedidos = PedidoDAO.obtener_todos()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)