import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-loading',
  templateUrl: './loading.component.html',
  styleUrls: ['./loading.component.scss']
})
export class LoadingComponent {
  @Input() message: string = 'Cargando...';
  @Input() show: boolean = true;
  @Input() type: 'overlay' | 'inline' = 'overlay';
  @Input() size: 'small' | 'medium' | 'large' = 'medium';
}
