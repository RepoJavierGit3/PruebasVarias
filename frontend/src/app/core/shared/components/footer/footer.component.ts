import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {
  currentYear: number = new Date().getFullYear();
  
  socialLinks = [
    { name: 'Facebook', icon: 'fa-facebook', url: '#' },
    { name: 'Twitter', icon: 'fa-twitter', url: '#' },
    { name: 'Instagram', icon: 'fa-instagram', url: '#' },
    { name: 'LinkedIn', icon: 'fa-linkedin', url: '#' }
  ];
  
  quickLinks = [
    { name: 'Inicio', url: '/' },
    { name: 'Productos', url: '/products' },
    { name: 'Sobre Nosotros', url: '/about' },
    { name: 'Contacto', url: '/contact' }
  ];
  
  legalLinks = [
    { name: 'Términos y Condiciones', url: '/terms' },
    { name: 'Política de Privacidad', url: '/privacy' },
    { name: 'Política de Cookies', url: '/cookies' }
  ];
}
