from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .external_services import GoogleBooksAPI
from .models import Categoria, Autor, Libro, Prestamo
from .serializers import (
    CategoriaSerializer, AutorSerializer, 
    LibroSerializer, PrestamoSerializer
)
# Importamos tu clase de throttling personalizada
from .throttles import BurstRateThrottle 

class CategoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para Categorías"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']
    ordering = ['nombre']


class AutorViewSet(viewsets.ModelViewSet):
    """ViewSet para Autores"""
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pais_origen']
    search_fields = ['nombre', 'apellido', 'biografia']
    ordering_fields = ['apellido', 'nombre', 'fecha_creacion']
    ordering = ['apellido', 'nombre']
    
    @action(detail=True, methods=['get'])
    def libros(self, request, pk=None):
        """Endpoint personalizado: /api/autores/{id}/libros/"""
        autor = self.get_object()
        libros = autor.libros.filter(activo=True)
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)


class LibroViewSet(viewsets.ModelViewSet):
    """ViewSet para Libros"""
    queryset = Libro.objects.filter(activo=True).select_related('autor', 'categoria')
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'categoria', 'autor']
    search_fields = ['titulo', 'isbn', 'descripcion']
    ordering_fields = ['titulo', 'precio', 'fecha_publicacion', 'valoracion']
    ordering = ['-fecha_creacion']
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Endpoint: /api/libros/disponibles/"""
        libros = self.queryset.filter(
            estado=Libro.DISPONIBLE,
            stock__gt=0
        )
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def actualizar_stock(self, request, pk=None):
        """POST /api/libros/{id}/actualizar_stock/"""
        libro = self.get_object()
        cantidad = request.data.get('cantidad', 0)
        
        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            return Response(
                {'error': 'La cantidad debe ser un número entero'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        libro.actualizar_stock(cantidad)
        serializer = self.get_serializer(libro)
        return Response(serializer.data)


class PrestamoViewSet(viewsets.ModelViewSet):
    """ViewSet para Préstamos"""
    queryset = Prestamo.objects.all().select_related('libro', 'usuario')
    serializer_class = PrestamoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estado', 'usuario']
    ordering_fields = ['fecha_prestamo', 'fecha_devolucion_esperada']
    ordering = ['-fecha_prestamo']
    
    def perform_create(self, serializer):
        """Al crear préstamo, asignar usuario actual y actualizar stock"""
        prestamo = serializer.save(usuario=self.request.user)
        prestamo.libro.actualizar_stock(-1) 
    
    @action(detail=True, methods=['post'])
    def devolver(self, request, pk=None):
        """POST /api/prestamos/{id}/devolver/"""
        prestamo = self.get_object()
        
        if prestamo.estado == Prestamo.DEVUELTO:
            return Response(
                {'error': 'Este préstamo ya fue devuelto'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        prestamo.fecha_devolucion_real = timezone.now()
        prestamo.estado = Prestamo.DEVUELTO
        prestamo.save()
        
        prestamo.libro.actualizar_stock(1)
        
        serializer = self.get_serializer(prestamo)
        return Response(serializer.data)

# --- FUNCIONES DE API ADICIONALES ---

@api_view(['POST'])
@permission_classes([IsAdminUser])
@throttle_classes([BurstRateThrottle]) # ← Protegemos la consulta externa
def importar_desde_google_books(request):
    """Importar libro desde Google Books por ISBN"""
    isbn = request.data.get('isbn')
    
    if not isbn:
        return Response({
            'error': 'El campo ISBN es requerido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Buscar en Google Books mediante el servicio externo
        data = GoogleBooksAPI.buscar_libro(isbn)
        
        if not data:
            return Response({
                'error': 'Libro no encontrado en Google Books'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'mensaje': 'Libro encontrado con éxito',
            'data': data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Error en la comunicación con Google Books: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)