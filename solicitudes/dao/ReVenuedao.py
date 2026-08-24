from typing import List, Optional
from solicitudes.models import Producto, Pedido


# ============================
#   DAO PARA PRODUCTOS/SERVICIOS
# ============================
class ProductoDAO:
    """Capa DAO para operaciones de Productos y Servicios del salón de eventos"""

    @staticmethod
    def obtener_todos() -> List[Producto]:
        return Producto.objects.all()

    @staticmethod
    def obtener_disponibles() -> List[Producto]:
        return Producto.objects.filter(disponible=True)

    @staticmethod
    def obtener_por_categoria(categoria: str) -> List[Producto]:
        """Filtra productos por categoría (Inmobiliario, Banquete, Música, etc.)"""
        return Producto.objects.filter(categoria=categoria, disponible=True)

    @staticmethod
    def obtener_por_id(producto_id: int) -> Optional[Producto]:
        try:
            return Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return None


# ============================
#   DAO PARA RESERVAS/PEDIDOS
# ============================
class PedidoDAO:
    """Capa DAO para operaciones de Reservas de eventos"""

    @staticmethod
    def obtener_todos() -> List[Pedido]:
        return Pedido.objects.all().order_by('-fecha_creacion')

    @staticmethod
    def obtener_por_fecha(fecha_evento) -> List[Pedido]:
        """Obtiene todas las reservas de un día específico"""
        return Pedido.objects.filter(fecha_evento=fecha_evento)

    @staticmethod
    def crear_reserva(cliente_nombre: str, cliente_email: str, fecha_evento, productos_ids: List[int]) -> Optional[Pedido]:
        """
        Crea una reserva con múltiples productos/servicios.
        Recalcula el total automáticamente gracias al método save() del modelo.
        """
        productos = Producto.objects.filter(id__in=productos_ids, disponible=True)

        if not productos.exists():
            return None

        pedido = Pedido.objects.create(
            cliente_nombre=cliente_nombre,
            cliente_email=cliente_email,
            fecha_evento=fecha_evento
        )

        pedido.productos.set(productos)
        pedido.save()  # recalcula total automáticamente

        return pedido

    @staticmethod
    def cambiar_estado(pedido_id: int, nuevo_estado: str) -> Optional[Pedido]:
        """Actualiza el estado de la reserva (Pendiente, Confirmado, Finalizado, Cancelado)"""
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.estado = nuevo_estado
            pedido.save()
            return pedido
        except Pedido.DoesNotExist:
            return None

    @staticmethod
    def agregar_producto(pedido_id: int, producto_id: int) -> Optional[Pedido]:
        """Agrega un producto/servicio a una reserva existente"""
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            producto = ProductoDAO.obtener_por_id(producto_id)

            if producto and producto.disponible:
                pedido.productos.add(producto)
                pedido.save()
                return pedido
            return None
        except Pedido.DoesNotExist:
            return None

    @staticmethod
    def eliminar_producto(pedido_id: int, producto_id: int) -> Optional[Pedido]:
        """Elimina un producto/servicio de una reserva existente"""
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            producto = ProductoDAO.obtener_por_id(producto_id)

            if producto:
                pedido.productos.remove(producto)
                pedido.save()
                return pedido
            return None
        except Pedido.DoesNotExist:
            return None