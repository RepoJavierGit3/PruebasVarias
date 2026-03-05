# Python + Angular + PostgreSQL Stack

## 🚀 Stack Completo de Desarrollo

Proyecto full stack con **Django REST Framework** + **Angular 17** + **PostgreSQL** + **Docker**.

## 📋 Características

- **Backend**: Django 4.2 + Django REST Framework + Celery
- **Frontend**: Angular 17 + TypeScript + Bootstrap 5
- **Database**: PostgreSQL 15 + Redis (cache/sesiones)
- **DevOps**: Docker + Docker Compose + Nginx
- **Testing**: pytest (backend) + Jasmine/Karma (frontend)
- **CI/CD**: GitHub Actions ready

## 🏗️ Arquitectura

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Angular   │    │   Django    │    │ PostgreSQL  │
│  Frontend   │◄──►│    API      │◄──►│  Database   │
│   (Nginx)   │    │  (DRF)      │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                   ┌─────────────┐
                   │    Redis    │
                   │ Cache/Queue │
                   └─────────────┘
```

## 🚀 Quick Start

### Prerrequisitos
- Docker & Docker Compose
- Git
- (Opcional) Node.js 18+ para desarrollo local

### 1. Clonar Repositorio
```bash
git clone https://github.com/tu-usuario/python-angular-postgres-stack.git
cd python-angular-postgres-stack
```

### 2. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 3. Iniciar Servicios
```bash
docker-compose up -d
```

### 4. Acceder a las Aplicaciones
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/
- **pgAdmin**: http://localhost:5050
- **Redis Commander**: http://localhost:8081

## 📁 Estructura del Proyecto

```
python-angular-postgres-stack/
├── README.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
├── scripts/
│   ├── setup-vm.sh
│   ├── start-dev.sh
│   └── deploy.sh
├── docs/
│   ├── setup-vm.md
│   ├── arquitectura.md
│   └── deployment.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── mi_proyecto/
│   │   ├── settings/
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── apps/
│       ├── core/
│       ├── users/
│       └── products/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── angular.json
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/
│   │   │   ├── shared/
│   │   │   ├── features/
│   │   │   └── layouts/
│   │   └── environments/
│   └── nginx.conf
└── infrastructure/
    ├── terraform/
    ├── kubernetes/
    └── ansible/
```

## 🛠️ Comandos Útiles

### Desarrollo
```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Acceder a contenedores
docker-compose exec backend bash
docker-compose exec postgres psql -U postgres
```

### Base de Datos
```bash
# Migraciones
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Backup
docker-compose exec postgres pg_dump -U postgres mi_proyecto_db > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres mi_proyecto_db < backup.sql
```

### Testing
```bash
# Backend tests
docker-compose exec backend python manage.py test

# Frontend tests
docker-compose exec frontend npm test
```

## 🔧 Configuración

### Variables de Entorno (.env)
```bash
# Database
DB_NAME=mi_proyecto_db
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=postgres
DB_PORT=5432

# Django
SECRET_KEY=django-insecure-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend

# Redis
REDIS_URL=redis://redis:6379/0

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

## 📚 Documentación

- [Setup en Máquina Virtual](docs/setup-vm.md)
- [Arquitectura Detallada](docs/arquitectura.md)
- [Guía de Deployment](docs/deployment.md)
- [API Documentation](http://localhost:8000/api/docs/)
- [Django Admin](http://localhost:8000/admin/)

## 🚀 Deployment

### Desarrollo
```bash
docker-compose up -d
```

### Producción
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes
```bash
kubectl apply -f infrastructure/kubernetes/
```

### Terraform
```bash
cd infrastructure/terraform/
terraform init
terraform plan
terraform apply
```

## 🧪 Testing

### Backend (Django)
```bash
# Ejecutar todos los tests
docker-compose exec backend python manage.py test

# Con coverage
docker-compose exec backend coverage run --source='.' manage.py test
docker-compose exec backend coverage report
```

### Frontend (Angular)
```bash
# Unit tests
docker-compose exec frontend npm test

# E2E tests
docker-compose exec frontend npm run e2e
```

## 📊 Monitoring

### Health Checks
```bash
# Ver estado de servicios
docker-compose ps

# Logs de errores
docker-compose logs backend | grep ERROR
docker-compose logs postgres | grep ERROR
```

### Métricas
- **Backend**: Django Debug Toolbar (development)
- **Frontend**: Angular DevTools
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

## 🤝 Contribuir

1. Fork el repositorio
2. Crear feature branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/python-angular-postgres-stack/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tu-usuario/python-angular-postgres-stack/discussions)
- **Email**: tu-email@example.com

## 🙏 Agradecimientos

- [Django](https://www.djangoproject.com/) - Backend framework
- [Angular](https://angular.io/) - Frontend framework
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Docker](https://www.docker.com/) - Containerization
- [Bootstrap](https://getbootstrap.com/) - CSS framework

---

## 🚀 Próximos Pasos

1. **Personalizar modelos** según tus necesidades
2. **Implementar autenticación** avanzada
3. **Añadir más features** al frontend
4. **Configurar CI/CD** con GitHub Actions
5. **Deploy a producción** en AWS/Azure

**¿Listo para empezar?** Revisa la sección [Quick Start](#-quick-start) arriba.
