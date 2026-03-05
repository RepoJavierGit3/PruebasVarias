# Angular Frontend Structure

## 📁 Estructura de Proyecto
```
mi-proyecto-frontend/
├── angular.json
├── package.json
├── tsconfig.json
├── Dockerfile
├── nginx.conf
├── src/
│   ├── main.ts
│   ├── index.html
│   ├── styles.scss
│   ├── app/
│   │   ├── app.module.ts
│   │   ├── app-routing.module.ts
│   │   ├── app.component.ts
│   │   ├── app.component.html
│   │   ├── app.component.scss
│   │   ├── core/
│   │   │   ├── guards/
│   │   │   │   ├── auth.guard.ts
│   │   │   │   └── admin.guard.ts
│   │   │   ├── interceptors/
│   │   │   │   ├── auth.interceptor.ts
│   │   │   │   └── error.interceptor.ts
│   │   │   └── services/
│   │   │       ├── auth.service.ts
│   │   │       ├── api.service.ts
│   │   │       └── notification.service.ts
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   │   ├── header/
│   │   │   │   ├── footer/
│   │   │   │   ├── loading/
│   │   │   │   └── pagination/
│   │   │   ├── pipes/
│   │   │   │   ├── search.pipe.ts
│   │   │   │   └── currency.pipe.ts
│   │   │   └── models/
│   │   │       ├── user.model.ts
│   │   │       ├── product.model.ts
│   │   │       └── category.model.ts
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   │   ├── components/
│   │   │   │   │   ├── login/
│   │   │   │   │   ├── register/
│   │   │   │   │   └── profile/
│   │   │   │   ├── auth.module.ts
│   │   │   │   └── auth-routing.module.ts
│   │   │   ├── products/
│   │   │   │   ├── components/
│   │   │   │   │   ├── product-list/
│   │   │   │   │   ├── product-detail/
│   │   │   │   │   ├── product-form/
│   │   │   │   │   └── category-list/
│   │   │   │   ├── services/
│   │   │   │   │   └── product.service.ts
│   │   │   │   ├── products.module.ts
│   │   │   │   └── products-routing.module.ts
│   │   │   └── dashboard/
│   │   │       ├── components/
│   │   │       │   ├── stats/
│   │   │       │   └── recent-products/
│   │   │       ├── dashboard.module.ts
│   │   │       └── dashboard-routing.module.ts
│   │   └── layouts/
│   │       ├── main-layout/
│   │       │   ├── main-layout.component.ts
│   │       │   ├── main-layout.component.html
│   │       │   └── main-layout.component.scss
│   │       └── auth-layout/
│   │           ├── auth-layout.component.ts
│   │           ├── auth-layout.component.html
│   │           └── auth-layout.component.scss
│   └── environments/
│       ├── environment.ts
│       └── environment.prod.ts
└── Dockerfile
```

## 📦 package.json
```json
{
  "name": "mi-proyecto-frontend",
  "version": "0.0.0",
  "scripts": {
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "watch": "ng build --watch --configuration development",
    "test": "ng test",
    "lint": "ng lint",
    "e2e": "ng e2e"
  },
  "private": true,
  "dependencies": {
    "@angular/animations": "^17.0.0",
    "@angular/common": "^17.0.0",
    "@angular/compiler": "^17.0.0",
    "@angular/core": "^17.0.0",
    "@angular/forms": "^17.0.0",
    "@angular/platform-browser": "^17.0.0",
    "@angular/platform-browser-dynamic": "^17.0.0",
    "@angular/router": "^17.0.0",
    "@angular/service-worker": "^17.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.14.0",
    "ngx-toastr": "^17.0.2",
    "ngx-bootstrap": "^12.0.0",
    "bootstrap": "^5.3.2",
    "@popperjs/core": "^2.11.8",
    "font-awesome": "^4.7.0"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^17.0.0",
    "@angular/cli": "^17.0.0",
    "@angular/compiler-cli": "^17.0.0",
    "@types/jasmine": "~5.1.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.57.0",
    "jasmine-core": "~5.1.0",
    "karma": "~6.4.0",
    "karma-chrome-launcher": "~3.2.0",
    "karma-coverage": "~2.2.0",
    "karma-jasmine": "~5.1.0",
    "karma-jasmine-html-reporter": "~2.1.0",
    "typescript": "~5.2.0"
  }
}
```

## 🌐 src/app/core/services/auth.service.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  password_confirm: string;
}

export interface AuthResponse {
  user: any;
  token: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/auth';
  private currentUserSubject = new BehaviorSubject<any>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    this.checkToken();
  }

  login(credentials: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login/`, credentials)
      .pipe(
        tap(response => {
          localStorage.setItem('token', response.token);
          localStorage.setItem('user', JSON.stringify(response.user));
          this.currentUserSubject.next(response.user);
        })
      );
  }

  register(userData: RegisterRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/register/`, userData)
      .pipe(
        tap(response => {
          localStorage.setItem('token', response.token);
          localStorage.setItem('user', JSON.stringify(response.user));
          this.currentUserSubject.next(response.user);
        })
      );
  }

  logout(): void {
    this.http.post(`${this.apiUrl}/logout/`, {}).subscribe();
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    this.currentUserSubject.next(null);
    this.router.navigate(['/auth/login']);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  checkToken(): void {
    const token = this.getToken();
    const user = localStorage.getItem('user');
    if (token && user) {
      this.currentUserSubject.next(JSON.parse(user));
    }
  }

  getCurrentUser(): any {
    return this.currentUserSubject.value;
  }
}
```

## 🌐 src/app/core/services/api.service.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  private getHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`
    });
  }

  get<T>(endpoint: string): Observable<T> {
    return this.http.get<T>(`${this.apiUrl}${endpoint}`, {
      headers: this.getHeaders()
    });
  }

  post<T>(endpoint: string, data: any): Observable<T> {
    return this.http.post<T>(`${this.apiUrl}${endpoint}`, data, {
      headers: this.getHeaders()
    });
  }

  put<T>(endpoint: string, data: any): Observable<T> {
    return this.http.put<T>(`${this.apiUrl}${endpoint}`, data, {
      headers: this.getHeaders()
    });
  }

  delete<T>(endpoint: string): Observable<T> {
    return this.http.delete<T>(`${this.apiUrl}${endpoint}`, {
      headers: this.getHeaders()
    });
  }

  uploadFile(endpoint: string, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    
    const headers = new HttpHeaders({
      'Authorization': `Token ${this.authService.getToken()}`
    });

    return this.http.post(`${this.apiUrl}${endpoint}`, formData, { headers });
  }
}
```

## 🌐 src/app/features/products/services/product.service.ts
```typescript
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  image?: string;
  category: number;
  category_name: string;
  stock: number;
  is_active: boolean;
  is_in_stock: boolean;
  created_by: number;
  created_by_name: string;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  created_at: string;
}

export interface ProductFilters {
  category?: number;
  search?: string;
  ordering?: string;
  page?: number;
}

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  constructor(private apiService: ApiService) {}

  getProducts(filters?: ProductFilters): Observable<any> {
    let params = '';
    if (filters) {
      const queryParams = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, value.toString());
        }
      });
      params = `?${queryParams.toString()}`;
    }
    return this.apiService.get<any>(`/products/${params}`);
  }

  getProduct(id: number): Observable<Product> {
    return this.apiService.get<Product>(`/products/${id}/`);
  }

  createProduct(productData: FormData): Observable<Product> {
    return this.apiService.post<Product>('/products/', productData);
  }

  updateProduct(id: number, productData: FormData): Observable<Product> {
    return this.apiService.put<Product>(`/products/${id}/`, productData);
  }

  deleteProduct(id: number): Observable<void> {
    return this.apiService.delete<void>(`/products/${id}/`);
  }

  getCategories(): Observable<Category[]> {
    return this.apiService.get<Category[]>('/products/categories/');
  }

  getMyProducts(): Observable<Product[]> {
    return this.apiService.get<Product[]>('/products/my-products/');
  }

  bulkUploadProducts(products: any[]): Observable<any> {
    return this.apiService.post<any>('/products/bulk-upload/', { products });
  }
}
```

## 🌐 src/app/features/products/components/product-list/product-list.component.ts
```typescript
import { Component, OnInit } from '@angular/core';
import { ProductService, Product, Category } from '../../services/product.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.scss']
})
export class ProductListComponent implements OnInit {
  products: Product[] = [];
  categories: Category[] = [];
  loading = false;
  currentPage = 1;
  totalPages = 1;
  filters = {
    category: undefined as number | undefined,
    search: '',
    ordering: '-created_at'
  };

  constructor(
    private productService: ProductService,
    private toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.loadCategories();
    this.loadProducts();
  }

  loadCategories(): void {
    this.productService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (error) => {
        this.toastr.error('Error cargando categorías');
      }
    });
  }

  loadProducts(): void {
    this.loading = true;
    const filters = { ...this.filters, page: this.currentPage };
    
    this.productService.getProducts(filters).subscribe({
      next: (response) => {
        this.products = response.results;
        this.totalPages = Math.ceil(response.count / 20);
        this.loading = false;
      },
      error: (error) => {
        this.toastr.error('Error cargando productos');
        this.loading = false;
      }
    });
  }

  onFilterChange(): void {
    this.currentPage = 1;
    this.loadProducts();
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.loadProducts();
  }

  deleteProduct(id: number): void {
    if (confirm('¿Estás seguro de eliminar este producto?')) {
      this.productService.deleteProduct(id).subscribe({
        next: () => {
          this.toastr.success('Producto eliminado correctamente');
          this.loadProducts();
        },
        error: (error) => {
          this.toastr.error('Error eliminando producto');
        }
      });
    }
  }

  onSearch(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.filters.search = target.value;
    this.onFilterChange();
  }

  onCategoryChange(event: Event): void {
    const target = event.target as HTMLSelectElement;
    this.filters.category = target.value ? Number(target.value) : undefined;
    this.onFilterChange();
  }

  onSortChange(event: Event): void {
    const target = event.target as HTMLSelectElement;
    this.filters.ordering = target.value;
    this.onFilterChange();
  }
}
```

## 🌐 src/app/features/products/components/product-list/product-list.component.html
```html
<div class="container-fluid">
  <div class="row mb-4">
    <div class="col-md-12">
      <h2>Lista de Productos</h2>
      <div class="row">
        <div class="col-md-3">
          <input 
            type="text" 
            class="form-control" 
            placeholder="Buscar productos..."
            (input)="onSearch($event)"
            [value]="filters.search"
          >
        </div>
        <div class="col-md-3">
          <select class="form-control" (change)="onCategoryChange($event)">
            <option value="">Todas las categorías</option>
            <option *ngFor="let category of categories" [value]="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
        <div class="col-md-3">
          <select class="form-control" (change)="onSortChange($event)">
            <option value="-created_at">Más recientes</option>
            <option value="created_at">Más antiguos</option>
            <option value="name">Nombre A-Z</option>
            <option value="-name">Nombre Z-A</option>
            <option value="price">Precio menor a mayor</option>
            <option value="-price">Precio mayor a menor</option>
          </select>
        </div>
        <div class="col-md-3">
          <a routerLink="/products/create" class="btn btn-primary w-100">
            <i class="fa fa-plus"></i> Nuevo Producto
          </a>
        </div>
      </div>
    </div>
  </div>

  <div class="row" *ngIf="loading">
    <div class="col-12 text-center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Cargando...</span>
      </div>
    </div>
  </div>

  <div class="row" *ngIf="!loading">
    <div class="col-md-4 mb-4" *ngFor="let product of products">
      <div class="card">
        <img 
          *ngIf="product.image" 
          [src]="'http://localhost:8000' + product.image" 
          class="card-img-top" 
          [alt]="product.name"
          style="height: 200px; object-fit: cover;"
        >
        <div class="card-body">
          <h5 class="card-title">{{ product.name }}</h5>
          <p class="card-text">{{ product.description | slice:0:100 }}...</p>
          <p class="card-text">
            <small class="text-muted">Categoría: {{ product.category_name }}</small>
          </p>
          <p class="card-text">
            <strong>${{ product.price | number:'1.2-2' }}</strong>
          </p>
          <p class="card-text">
            <span 
              class="badge" 
              [class]="product.is_in_stock ? 'bg-success' : 'bg-danger'"
            >
              {{ product.is_in_stock ? 'En stock' : 'Sin stock' }}
            </span>
            <span class="badge bg-info">Stock: {{ product.stock }}</span>
          </p>
          <div class="btn-group w-100" role="group">
            <button 
              class="btn btn-outline-primary btn-sm"
              routerLink="/products/{{ product.id }}"
            >
              <i class="fa fa-eye"></i> Ver
            </button>
            <button 
              class="btn btn-outline-warning btn-sm"
              routerLink="/products/edit/{{ product.id }}"
            >
              <i class="fa fa-edit"></i> Editar
            </button>
            <button 
              class="btn btn-outline-danger btn-sm"
              (click)="deleteProduct(product.id)"
            >
              <i class="fa fa-trash"></i> Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="row mt-4" *ngIf="totalPages > 1">
    <div class="col-12">
      <nav aria-label="Page navigation">
        <ul class="pagination justify-content-center">
          <li class="page-item" [class.disabled]="currentPage === 1">
            <a class="page-link" (click)="onPageChange(currentPage - 1)">Anterior</a>
          </li>
          <li 
            class="page-item" 
            *ngFor="let page of getPages()" 
            [class.active]="page === currentPage"
          >
            <a class="page-link" (click)="onPageChange(page)">{{ page }}</a>
          </li>
          <li class="page-item" [class.disabled]="currentPage === totalPages">
            <a class="page-link" (click)="onPageChange(currentPage + 1)">Siguiente</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</div>
```

## 🐳 Dockerfile
```dockerfile
# Multi-stage build
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build --prod

# Production stage
FROM nginx:alpine

# Copy built app
COPY --from=builder /app/dist/mi-proyecto-frontend /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## 🐳 nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        # Enable gzip compression
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

        # Handle Angular routing
        location / {
            try_files $uri $uri/ /index.html;
        }

        # API proxy to backend
        location /api/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Cache static files
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```
