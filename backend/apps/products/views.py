from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from django.contrib.auth import get_user_model
from .models import Product, Category, ProductReview, ProductVariant, Wishlist
from .serializers import (
    ProductSerializer, ProductListSerializer, ProductCreateUpdateSerializer,
    CategorySerializer, ProductReviewSerializer, ProductVariantSerializer,
    WishlistSerializer, WishlistCreateSerializer
)

User = get_user_model()


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand', 'condition', 'is_featured']
    search_fields = ['name', 'description', 'short_description', 'brand', 'tags']
    ordering_fields = ['name', 'price', 'created_at', 'view_count', 'sales_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductCreateUpdateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by stock
        in_stock = self.request.query_params.get('in_stock')
        if in_stock == 'true':
            queryset = queryset.filter(
                Q(track_inventory=False) | Q(stock__gt=0)
            )
        
        # Filter by rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rating')
            ).filter(avg_rating__gte=min_rating)
        
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_products(request):
    """
    Get products created by the current user
    """
    products = Product.objects.filter(created_by=request.user, is_active=True)
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_upload_products(request):
    """
    Bulk upload products
    """
    products_data = request.data.get('products', [])
    created_products = []
    errors = []
    
    for index, product_data in enumerate(products_data):
        serializer = ProductCreateUpdateSerializer(
            data=product_data,
            context={'request': request}
        )
        if serializer.is_valid():
            product = serializer.save()
            created_products.append(ProductListSerializer(product).data)
        else:
            errors.append({
                'index': index,
                'errors': serializer.errors
            })
    
    response_data = {
        'message': f'Se crearon {len(created_products)} productos',
        'products': created_products
    }
    
    if errors:
        response_data['errors'] = errors
        response_data['message'] += f', {len(errors)} productos con errores'
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_product_review(request, product_id):
    """
    Add a review to a product
    """
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if user already reviewed this product
    if ProductReview.objects.filter(product=product, user=request.user).exists():
        return Response(
            {'error': 'Ya has reseñado este producto'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ProductReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(product=product, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_wishlist(request, product_id):
    """
    Toggle product in user's default wishlist
    """
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user,
        defaults={'name': 'My Wishlist'}
    )
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        return Response({'message': 'Producto eliminado de la wishlist'})
    else:
        wishlist.products.add(product)
        return Response({'message': 'Producto agregado a la wishlist'})


class WishlistListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WishlistSerializer
        return WishlistCreateSerializer


class WishlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return WishlistCreateSerializer
        return WishlistSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_products(request):
    """
    Get featured products
    """
    limit = int(request.query_params.get('limit', 12))
    products = Product.objects.filter(is_active=True, is_featured=True)[:limit]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_stats(request):
    """
    Get product statistics
    """
    stats = {
        'total_products': Product.objects.filter(is_active=True).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'featured_products': Product.objects.filter(is_active=True, is_featured=True).count(),
        'low_stock_products': Product.objects.filter(
            is_active=True, 
            track_inventory=True, 
            stock__lte=models.F('stock_alert')
        ).count(),
    }
    
    if request.user.is_authenticated:
        stats['my_products'] = Product.objects.filter(
            created_by=request.user, 
            is_active=True
        ).count()
    
    return Response(stats)
