# Backend Django - Mi Proyecto

## 🚀 Stack de Desarrollo

Backend API construido con **Django 4.2** + **Django REST Framework** + **PostgreSQL** + **Redis** + **Celery**.

## 📋 Características

- **Framework**: Django 4.2 + Django REST Framework 3.14
- **Base de Datos**: PostgreSQL 15 con Redis para cache
- **Autenticación**: Token Authentication + JWT
- **Arquitectura**: Apps modulares (core, users, products)
- **Tareas Asíncronas**: Celery + Redis
- **Contenerización**: Docker + Docker Compose
- **Monitoreo**: Health checks, logging, pgAdmin, Redis Commander

## 🏗️ Estructura del Proyecto

```
backend/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
├── mi_proyecto/
│   ├── __init__.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── production.py
│       └── testing.py
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── apps.py
│   │   ├── signals.py
│   │   └── admin.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── apps.py
│   │   ├── signals.py
│   │   └── admin.py
│   └── products/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── urls.py
│       ├── apps.py
│       └── admin.py
├── nginx/
│   ├── nginx.conf
│   └── default.conf
├── scripts/
│   └── init.sql
├── static/
├── media/
└── logs/
```

## 🚀 Quick Start

### 1. Clonar y Configurar
```bash
cd PruebasVarias/backend
cp .env.example .env
# Editar .env con tus configuraciones
```

### 2. Iniciar Servicios
```bash
docker-compose up -d
```

### 3. Acceder a las Aplicaciones
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/docs/
- **Health Check**: http://localhost:8000/api/core/health/
- **pgAdmin**: http://localhost:5050
- **Redis Commander**: http://localhost:8081

## 📡 Endpoints Principales

### Autenticación
- `POST /api/auth/register/` - Registro de usuario
- `POST /api/auth/login/` - Inicio de sesión
- `POST /api/auth/logout/` - Cierre de sesión
- `GET /api/auth/profile/` - Perfil de usuario
- `POST /api/auth/change-password/` - Cambiar contraseña

### Productos
- `GET /api/products/` - Listar productos
- `POST /api/products/` - Crear producto
- `GET /api/products/{id}/` - Detalle de producto
- `PUT /api/products/{id}/` - Actualizar producto
- `DELETE /api/products/{id}/` - Eliminar producto
- `GET /api/products/categories/` - Listar categorías
- `POST /api/products/bulk-upload/` - Carga masiva

### Core
- `GET /api/core/health/` - Health check
- `GET /api/core/system-info/` - Información del sistema
- `GET /api/core/configurations/` - Configuraciones (admin)

## 🛠️ Comandos Útiles

### Docker Compose
```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f redis

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Acceder a contenedores
docker-compose exec backend bash
docker-compose exec postgres psql -U postgres -d mi_proyecto_db
docker-compose exec redis redis-cli
```

### Django Management
```bash
# Migraciones
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Recolectar archivos estáticos
docker-compose exec backend python manage.py collectstatic --noinput

# Shell de Django
docker-compose exec backend python manage.py shell

# Tests
docker-compose exec backend python manage.py test
```

### Celery
```bash
# Ver tareas activas
docker-compose exec celery celery -A mi_proyecto inspect active

# Ver estadísticas
docker-compose exec celery celery -A mi_proyecto inspect stats
```

## 🔧 Configuración

### Variables de Entorno Principales
```bash
# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=True  # False en producción
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos
DB_NAME=mi_proyecto_db
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=postgres
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
docker-compose exec backend python manage.py test

# Con coverage
docker-compose exec backend coverage run --source='.' manage.py test
docker-compose exec backend coverage report

# Tests de una app específica
docker-compose exec backend python manage.py test apps.users
docker-compose exec backend python manage.py test apps.products
```

## 📊 Monitoreo

### Health Checks
```bash
# Ver estado de servicios
docker-compose ps

# Health check del backend
curl http://localhost:8000/api/core/health/

# Logs de errores
docker-compose logs backend | grep ERROR
```

### Métricas
- **Backend**: Django Debug Toolbar (development)
- **Database**: pgAdmin (http://localhost:5050)
- **Cache**: Redis Commander (http://localhost:8081)

## 🔐 Seguridad

### En Producción
- Cambiar `SECRET_KEY` y contraseñas por defecto
- Configurar `DEBUG=False`
- Usar HTTPS con certificados SSL
- Configurar firewalls y redes privadas
- Implementar rate limiting
- Usar variables de entorno seguras

### Best Practices
- Usar contraseñas fuertes
- Rotar claves regularmente
- Implementar backups automáticos
- Monitorear accesos sospechosos
- Mantener dependencias actualizadas

## 🚀 Deployment

### Desarrollo
```bash
docker-compose up -d
```

### Producción
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Documentación

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 Contribuir

1. Fork el repositorio
2. Crear feature branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**¿Listo para empezar?** Revisa la sección [Quick Start](#-quick-start) arriba.
