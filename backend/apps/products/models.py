from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from apps.core.models import BaseModel

User = get_user_model()


class Category(BaseModel):
    """
    Product category model
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_product_count(self):
        return Product.objects.filter(category=self, is_active=True).count()


class Product(BaseModel):
    """
    Product model
    """
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True)
    images = models.JSONField(default=list, blank=True)  # Store multiple image URLs
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    barcode = models.CharField(max_length=50, blank=True)
    track_inventory = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    stock_alert = models.PositiveIntegerField(default=5)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dimensions = models.JSONField(default=dict, blank=True)  # {length, width, height}
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    tags = models.JSONField(default=list, blank=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    requires_shipping = models.BooleanField(default=True)
    taxable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    view_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['price']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure unique slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.name)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.stock > 0 if self.track_inventory else True

    @property
    def is_low_stock(self):
        return self.stock <= self.stock_alert if self.track_inventory else False

    @property
    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return round((self.compare_price - self.price) / self.compare_price * 100, 2)
        return 0

    def get_absolute_url(self):
        return f"/products/{self.slug}/"

    def get_main_image_url(self):
        if self.image:
            return self.image.url
        elif self.images:
            return self.images[0]
        return f"https://via.placeholder.com/300x300?text={self.name}"


class ProductReview(BaseModel):
    """
    Product review model
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_verified = models.BooleanField(default=False)  # Verified purchase
    helpful_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.user.username} - {self.rating} stars"


class ProductVariant(BaseModel):
    """
    Product variant model (for size, color, etc.)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)  # e.g., "Small", "Red", "Cotton"
    sku = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='variants/', blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'
        ordering = ['position', 'name']

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class Wishlist(BaseModel):
    """
    User wishlist model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    products = models.ManyToManyField(Product, related_name='wishlists')
    name = models.CharField(max_length=100, default='My Wishlist')
    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return f"{self.user.username} - {self.name}"
