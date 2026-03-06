# Frontend Angular - Mi Proyecto

## 📋 Descripción

Frontend moderno desarrollado con Angular 17, TypeScript y Bootstrap 5 para el proyecto Mi Proyecto.

## 🛠️ Stack Tecnológico

- **Framework**: Angular 17
- **Lenguaje**: TypeScript
- **Estilos**: SCSS + Bootstrap 5
- **Build Tool**: Angular CLI
- **Package Manager**: npm
- **Contenedor**: Docker + Nginx

## 📁 Estructura del Proyecto

```
src/
├── app/
│   ├── core/                 # Módulo principal con servicios compartidos
│   │   ├── services/         # Servicios reutilizables
│   │   │   ├── auth.service.ts
│   │   │   └── api.service.ts
│   │   ├── guards/           # Guards de rutas
│   │   │   ├── auth.guard.ts
│   │   │   └── admin.guard.ts
│   │   ├── interceptors/     # Interceptores HTTP
│   │   │   ├── auth.interceptor.ts
│   │   │   └── error.interceptor.ts
│   │   └── shared/          # Componentes compartidos
│   │       ├── components/
│   │       ├── pipes/
│   │       └── models/
│   ├── features/             # Módulos de funcionalidades específicas
│   │   ├── auth/            # Autenticación y usuarios
│   │   └── products/        # Gestión de productos
│   ├── app.module.ts          # Módulo principal
│   ├── app-routing.module.ts  # Configuración de rutas
│   └── app.component.ts       # Componente raíz
├── environments/             # Variables de entorno
├── assets/                  # Archivos estáticos
└── styles.scss              # Estilos globales
```

## 🚀 Instalación y Desarrollo

### Prerrequisitos
- Node.js 18+
- npm 9+

### Instalación
```bash
npm install
```

### Modo Desarrollo
```bash
npm start
```
La aplicación estará disponible en `http://localhost:4200`

### Build Producción
```bash
npm run build
```
Los archivos compilados estarán en `dist/`

## 🐳 Docker

### Construir Imagen
```bash
docker build -t mi-proyecto-frontend .
```

### Ejecutar Contenedor
```bash
docker run -p 80:80 mi-proyecto-frontend
```

### Docker Compose
```bash
docker-compose -f docker-compose.yml up
```

## 🌐 Funcionalidades

### ✅ Implementadas
- **Autenticación**: Login, registro, logout
- **Gestión de Usuarios**: Perfil de usuario
- **Productos**: Listado, detalle, búsqueda
- **Rutas Protegidas**: Guards de autenticación
- **Interceptores HTTP**: Manejo de tokens y errores
- **Diseño Responsivo**: Mobile-first con Bootstrap
- **Notificaciones**: Toastr para feedback al usuario

### 🔄 En Progreso
- **Panel de Administración**
- **Gestión Avanzada de Productos**
- **Sistema de Reviews**
- **Carrito de Compras**

## 🔧 Configuración

### Variables de Entorno
- `environment.ts`: Desarrollo
- `environment.prod.ts`: Producción

### API Backend
La aplicación se conecta al backend Django en:
- Desarrollo: `http://192.168.100.27:8000/api`
- Producción: `https://tu-dominio.com/api`

## 📱 Componentes Principales

### Autenticación
- `LoginComponent`: Formulario de inicio de sesión
- `RegisterComponent`: Formulario de registro
- `ProfileComponent`: Perfil de usuario

### Productos
- `ProductListComponent`: Listado de productos
- `ProductDetailComponent`: Detalle de producto
- `ProductFormComponent`: Formulario de producto

### Compartidos
- `HeaderComponent`: Navegación principal
- `FooterComponent`: Pie de página
- `LoadingComponent`: Indicador de carga
- `PaginationComponent`: Paginación de resultados

## 🔐 Seguridad

- **Tokens JWT**: Autenticación con tokens
- **Guards**: Protección de rutas
- **Interceptores**: Inyección automática de headers
- **CORS**: Configuración para API externa
- **Headers de Seguridad**: Configuración Nginx

## 🎨 Estilos

- **Bootstrap 5**: Framework CSS base
- **SCSS**: Preprocesador para estilos personalizados
- **Variables CSS**: Diseño consistente
- **Responsive**: Mobile-first approach
- **Componentes Personalizados**: Extensión de Bootstrap

## 📊 Rendimiento

- **Lazy Loading**: Módulos cargados bajo demanda
- **Tree Shaking**: Eliminación de código no utilizado
- **Bundle Optimization**: Configuración de producción
- **Caching**: Headers de caché para assets estáticos
- **Gzip**: Compresión de respuestas

## 🧪 Testing

### Ejecutar Tests Unitarios
```bash
npm test
```

### Ejecutar E2E Tests
```bash
npm run e2e
```

### Linting
```bash
npm run lint
```

## 📝 Scripts Disponibles

- `npm start`: Servidor de desarrollo
- `npm run build`: Build de producción
- `npm run watch`: Build con watch
- `npm test`: Ejecutar tests unitarios
- `npm run e2e`: Ejecutar tests e2e
- `npm run lint`: Análisis de código

## 🚀 Despliegue

### Producción
1. Build: `npm run build`
2. Copiar archivos de `dist/` al servidor
3. Configurar Nginx/Apache para SPA routing

### Docker
1. Build imagen: `docker build -t frontend .`
2. Ejecutar: `docker run -p 80:80 frontend`

### Kubernetes
```bash
kubectl apply -f k8s/
```

## 🔧 Desarrollo

### Agregar Nuevo Componente
```bash
ng generate component components/nuevo-componente
```

### Agregar Nuevo Servicio
```bash
ng generate service services/nuevo-servicio
```

### Agregar Nuevo Módulo
```bash
ng generate module features/nuevo-modulo
```

## 🐛 Troubleshooting

### Problemas Comunes
1. **Errores de CORS**: Verificar configuración de API
2. **Build lento**: Usar `npm ci` en lugar de `npm install`
3. **Rutas no funcionan**: Verificar AppRoutingModule
4. **Estilos no aplican**: Revisar orden de imports CSS

### Debug Mode
```bash
ng serve --configuration development
```

## 📚 Documentación Adicional

- [Angular Documentation](https://angular.io/docs)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [RxJS Documentation](https://rxjs.dev/api)

## 🤝 Contribución

1. Fork del repositorio
2. Crear feature branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit de cambios: `git commit -am "Add nueva funcionalidad"`
4. Push al branch: `git push origin feature/nueva-funcionalidad`
5. Pull Request

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles
