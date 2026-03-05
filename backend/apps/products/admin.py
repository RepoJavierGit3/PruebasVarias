from django.contrib import admin
from .models import Product, Category, ProductReview, ProductVariant, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'product_count', 'is_active', 'order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    readonly_fields = ['created_at', 'updated_at']

    def product_count(self, obj):
        return obj.get_product_count()


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ['user', 'rating', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price', 'stock', 'is_active', 
        'is_featured', 'created_by', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_featured', 'category', 'brand', 
        'condition', 'track_inventory'
    ]
    search_fields = ['name', 'description', 'sku', 'brand']
    ordering = ['-created_at']
    readonly_fields = [
        'slug', 'created_by', 'view_count', 'sales_count',
        'created_at', 'updated_at'
    ]
    filter_horizontal = []
    inlines = [ProductVariantInline, ProductReviewInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'category')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price', 'cost')
        }),
        ('Inventory', {
            'fields': ('track_inventory', 'stock', 'stock_alert', 'sku', 'barcode')
        }),
        ('Media', {
            'fields': ('image', 'images')
        }),
        ('Attributes', {
            'fields': ('brand', 'condition', 'weight', 'dimensions', 'tags')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description')
        }),
        ('Settings', {
            'fields': (
                'requires_shipping', 'taxable', 'is_active', 'is_featured'
            )
        }),
        ('Statistics', {
            'fields': (
                'view_count', 'sales_count', 'created_by', 
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified', 'helpful_count', 'created_at']
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = ['product__name', 'user__username', 'title', 'content']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'sku', 'price', 'stock', 'position']
    list_filter = ['product', 'position']
    search_fields = ['product__name', 'name', 'sku']
    ordering = ['product', 'position', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'products_count', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['user__username', 'name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['products']

    def products_count(self, obj):
        return obj.products.count()
