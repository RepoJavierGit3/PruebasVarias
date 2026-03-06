import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RouterModule.forChild([
      { path: '', component: AdminDashboardComponent }
    ])
  ]
})
export class AdminModule { }

// Temporary placeholder component
export class AdminDashboardComponent {
  constructor() {}
}
