import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../../../../core/services/api.service';

export interface Product {
  id: number;
  name: string;
  slug: string;
  short_description: string;
  price: string;
  compare_price: string | null;
  image: string | null;
  category_name: string;
  brand: string;
  is_active: boolean;
  is_featured: boolean;
  main_image_url: string;
  is_in_stock: boolean;
  discount_percentage: string;
  average_rating: number;
  reviews_count: number;
  created_at: string;
}

export interface ProductResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Product[];
}

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.scss']
})
export class ProductListComponent implements OnInit {
  products: Product[] = [];
  loading = true;
  error = '';
  currentPage = 1;
  totalPages = 1;
  totalItems = 0;
  itemsPerPage = 12;
  searchTerm = '';
  selectedCategory = '';
  sortBy = 'name';
  sortOrder = 'asc';

  categories = [
    { value: '', label: 'Todas las categorías' },
    { value: 'electronics', label: 'Electrónica' },
    { value: 'clothing', label: 'Ropa' },
    { value: 'books', label: 'Libros' },
    { value: 'home', label: 'Hogar' },
    { value: 'sports', label: 'Deportes' }
  ];

  sortOptions = [
    { value: 'name', label: 'Nombre' },
    { value: 'price', label: 'Precio' },
    { value: 'created_at', label: 'Fecha' },
    { value: 'rating', label: 'Calificación' }
  ];

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadProducts();
    this.setupQueryParams();
  }

  private setupQueryParams(): void {
    this.route.queryParams.subscribe(params => {
      this.searchTerm = params['search'] || '';
      this.selectedCategory = params['category'] || '';
      this.sortBy = params['sort'] || 'name';
      this.sortOrder = params['order'] || 'asc';
      this.currentPage = parseInt(params['page']) || 1;
      
      this.loadProducts();
    });
  }

  loadProducts(): void {
    this.loading = true;
    this.error = '';

    const params = {
      page: this.currentPage,
      page_size: this.itemsPerPage,
      search: this.searchTerm,
      category: this.selectedCategory,
      ordering: `${this.sortOrder === 'desc' ? '-' : ''}${this.sortBy}`
    };

    this.apiService.get<ProductResponse>('/products/', params).subscribe({
      next: (response) => {
        this.products = response.results;
        this.totalItems = response.count;
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Error al cargar los productos. Por favor, inténtalo de nuevo.';
        this.loading = false;
        console.error('Error loading products:', error);
      }
    });
  }

  onSearch(): void {
    this.currentPage = 1;
    this.updateQueryParams();
  }

  onFilter(): void {
    this.currentPage = 1;
    this.updateQueryParams();
  }

  onSort(): void {
    this.updateQueryParams();
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.updateQueryParams();
  }

  private updateQueryParams(): void {
    const queryParams: any = {};
    
    if (this.searchTerm) queryParams.search = this.searchTerm;
    if (this.selectedCategory) queryParams.category = this.selectedCategory;
    if (this.sortBy !== 'name') queryParams.sort = this.sortBy;
    if (this.sortOrder !== 'asc') queryParams.order = this.sortOrder;
    if (this.currentPage > 1) queryParams.page = this.currentPage;

    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: queryParams,
      queryParamsHandling: 'merge'
    });
  }

  goToProductDetail(product: Product): void {
    this.router.navigate(['/products', product.slug]);
  }

  addToCart(product: Product): void {
    // TODO: Implement cart functionality
    console.log('Added to cart:', product.name);
  }

  toggleFavorite(product: Product): void {
    // TODO: Implement favorite functionality
    console.log('Toggled favorite:', product.name);
  }

  getDiscountPrice(product: Product): string {
    if (product.discount_percentage && product.discount_percentage !== '0.00') {
      const price = parseFloat(product.price);
      const discount = parseFloat(product.discount_percentage);
      const discountedPrice = price * (1 - discount / 100);
      return discountedPrice.toFixed(2);
    }
    return product.price;
  }

  hasDiscount(product: Product): boolean {
    return product.discount_percentage && 
           product.discount_percentage !== '0.00' && 
           parseFloat(product.discount_percentage) > 0;
  }

  getRatingStars(rating: number): number[] {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const stars = [];
    
    for (let i = 0; i < fullStars; i++) {
      stars.push(1);
    }
    
    if (hasHalfStar) {
      stars.push(0.5);
    }
    
    const emptyStars = 5 - stars.length;
    for (let i = 0; i < emptyStars; i++) {
      stars.push(0);
    }
    
    return stars;
  }
}
