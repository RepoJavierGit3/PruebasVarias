from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListCreateView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail-slug'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('my-products/', views.my_products, name='my-products'),
    path('bulk-upload/', views.bulk_upload_products, name='bulk-upload'),
    path('<int:product_id>/review/', views.add_product_review, name='add-review'),
    path('<int:product_id>/wishlist/', views.toggle_wishlist, name='toggle-wishlist'),
    path('wishlists/', views.WishlistListCreateView.as_view(), name='wishlist-list'),
    path('wishlists/<int:pk>/', views.WishlistDetailView.as_view(), name='wishlist-detail'),
    path('featured/', views.featured_products, name='featured-products'),
    path('stats/', views.product_stats, name='product-stats'),
]
