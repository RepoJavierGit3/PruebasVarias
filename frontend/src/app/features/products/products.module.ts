import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { ProductListComponent } from './components/list/product-list.component';
import { PaginationComponent } from '../../core/shared/components/pagination/pagination.component';
import { LoadingComponent } from '../../core/shared/components/loading/loading.component';

@NgModule({
  declarations: [
    ProductListComponent,
    PaginationComponent,
    LoadingComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild([
      { path: '', component: ProductListComponent }
    ])
  ],
  exports: [
    ProductListComponent,
    PaginationComponent,
    LoadingComponent
  ]
})
export class ProductsModule { }
