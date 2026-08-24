from rest_framework import serializers
from solicitudes.models import Producto, Pedido


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    # Productos como objetos completos (solo lectura)
    productos = ProductoSerializer(many=True, read_only=True)

    # Para recibir solo los IDs de productos al crear una reserva
    productos_ids = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = Pedido
        fields = [
            'id',
            'cliente_nombre',
            'cliente_email',
            'fecha_evento',
            'fecha_creacion',
            'estado',
            'productos',       # objetos completos
            'productos_ids',   # solo IDs para creación
            'total'
        ]

    def create(self, validated_data):
        """
        Crea una reserva con múltiples productos.
        El total se calcula automáticamente gracias al método save() del modelo.
        """
        productos_ids = validated_data.pop('productos_ids')
        pedido = Pedido.objects.create(**validated_data)
        pedido.productos.set(productos_ids)
        pedido.save()  # recalcula total
        return pedido