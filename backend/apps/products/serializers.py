from rest_framework import serializers
from .models import Product, Category, ProductReview, ProductVariant, Wishlist


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'image', 'parent', 'children',
            'product_count', 'is_active', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_product_count(self, obj):
        return obj.get_product_count()

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            'id', 'name', 'sku', 'price', 'stock', 'image', 'position',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.CharField(source='user.get_avatar_url', read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            'id', 'user', 'user_avatar', 'rating', 'title', 'content',
            'is_verified', 'helpful_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'is_verified', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    main_image_url = serializers.SerializerMethodField()
    is_in_stock = serializers.BooleanField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'compare_price', 'cost', 'image', 'images',
            'category', 'category_name', 'brand', 'sku', 'barcode',
            'track_inventory', 'stock', 'stock_alert', 'weight',
            'dimensions', 'condition', 'tags', 'seo_title',
            'seo_description', 'requires_shipping', 'taxable',
            'is_active', 'is_featured', 'created_by', 'created_by_name',
            'view_count', 'sales_count', 'main_image_url', 'is_in_stock',
            'is_low_stock', 'discount_percentage', 'variants', 'reviews',
            'average_rating', 'reviews_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'slug', 'created_by', 'view_count', 'sales_count',
            'created_at', 'updated_at'
        ]

    def get_main_image_url(self, obj):
        return obj.get_main_image_url()

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 2)
        return 0

    def get_reviews_count(self, obj):
        return obj.reviews.count()


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_image_url = serializers.SerializerMethodField()
    is_in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price',
            'compare_price', 'image', 'category_name', 'brand',
            'is_active', 'is_featured', 'main_image_url', 'is_in_stock',
            'discount_percentage', 'average_rating', 'reviews_count',
            'created_at'
        ]

    def get_main_image_url(self, obj):
        return obj.get_main_image_url()

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 2)
        return 0

    def get_reviews_count(self, obj):
        return obj.reviews.count()


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'short_description', 'price',
            'compare_price', 'cost', 'image', 'category', 'brand',
            'sku', 'barcode', 'track_inventory', 'stock',
            'stock_alert', 'weight', 'dimensions', 'condition',
            'tags', 'seo_title', 'seo_description',
            'requires_shipping', 'taxable', 'is_active', 'is_featured'
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class WishlistSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = [
            'id', 'name', 'products', 'products_count', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_products_count(self, obj):
        return obj.products.count()


class WishlistCreateSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Wishlist
        fields = ['name', 'is_public', 'product_ids']

    def create(self, validated_data):
        product_ids = validated_data.pop('product_ids', [])
        user = self.context['request'].user
        
        wishlist = Wishlist.objects.create(user=user, **validated_data)
        
        if product_ids:
            wishlist.products.set(product_ids)
        
        return wishlist
