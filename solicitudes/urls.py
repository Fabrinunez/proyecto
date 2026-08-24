from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API REST
router = DefaultRouter()
router.register(r'api/productos', views.ProductoViewSet, basename='api_productos')
router.register(r'api/reservas', views.PedidoViewSet, basename='api_reservas')

urlpatterns = [
    # Rutas Web (HTML)
    path('', views.home_view, name='home'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('reservas/', views.reservas_view, name='reservas'),
    path('reserva/nueva/', views.crear_reserva_action, name='crear_reserva'),
    path('reserva/<int:pedido_id>/estado/', views.cambiar_estado_action, name='cambiar_estado'),

    # Rutas API REST
    path('', include(router.urls)),
]