# Docker Compose - Stack Completo

## 🐳 docker-compose.yml
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: postgres_db
    environment:
      POSTGRES_DB: mi_proyecto_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres123
      POSTGRES_HOST_AUTH_METHOD: trust
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - app_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis for caching and sessions
  redis:
    image: redis:7-alpine
    container_name: redis_cache
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Django Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: django_backend
    environment:
      - DEBUG=True
      - SECRET_KEY=django-insecure-development-key-change-in-production
      - DB_NAME=mi_proyecto_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres123
      - DB_HOST=postgres
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
      - ALLOWED_HOSTS=localhost,127.0.0.1,backend
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app_network
    restart: unless-stopped
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             python manage.py runserver 0.0.0.0:8000"

  # Celery Worker
  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: celery_worker
    environment:
      - DEBUG=True
      - SECRET_KEY=django-insecure-development-key-change-in-production
      - DB_NAME=mi_proyecto_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres123
      - DB_HOST=postgres
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./backend:/app
    depends_on:
      - postgres
      - redis
    networks:
      - app_network
    restart: unless-stopped
    command: celery -A mi_proyecto worker -l info

  # Celery Beat (Scheduler)
  celery_beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: celery_beat
    environment:
      - DEBUG=True
      - SECRET_KEY=django-insecure-development-key-change-in-production
      - DB_NAME=mi_proyecto_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres123
      - DB_HOST=postgres
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./backend:/app
    depends_on:
      - postgres
      - redis
    networks:
      - app_network
    restart: unless-stopped
    command: celery -A mi_proyecto beat -l info

  # Angular Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: angular_frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app_network
    restart: unless-stopped

  # pgAdmin (Database Management)
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@mi-proyecto.com
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    depends_on:
      - postgres
    networks:
      - app_network
    restart: unless-stopped

  # Redis Commander (Redis Management)
  redis_commander:
    image: rediscommander/redis-commander:latest
    container_name: redis_commander
    environment:
      REDIS_HOSTS: local:redis:6379
    ports:
      - "8081:8081"
    depends_on:
      - redis
    networks:
      - app_network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
  pgadmin_data:

networks:
  app_network:
    driver: bridge
```

## 🐳 backend/Dockerfile
```dockerfile
# Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Expose port
EXPOSE 8000

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mi_proyecto.wsgi:application"]
```

## 🐳 init.sql (Database Initialization)
```sql
-- Create additional schemas if needed
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create initial data
-- This file is executed when the PostgreSQL container starts for the first time

-- Example: Create a sample category (this will be managed by Django migrations)
-- INSERT INTO categories (name, description, created_at) 
-- VALUES ('Electrónica', 'Productos electrónicos y gadgets', NOW());
```

## 🐳 .env (Environment Variables)
```bash
# Database Configuration
DB_NAME=mi_proyecto_db
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=postgres
DB_PORT=5432

# Django Configuration
SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Media Files (Optional - for production)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
```

## 🐳 docker-compose.prod.yml (Production)
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network
    restart: always
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - app_network
    restart: always
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 256M
        reservations:
          memory: 128M

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=postgres
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
      - ALLOWED_HOSTS=${DOMAIN}
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - postgres
      - redis
    networks:
      - app_network
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=postgres
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    networks:
      - app_network
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 256M
        reservations:
          memory: 128M

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - backend
    networks:
      - app_network
    restart: always
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 256M
        reservations:
          memory: 128M

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.prod.conf:/etc/nginx/nginx.conf
      - static_volume:/var/www/static
      - media_volume:/var/www/media
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    networks:
      - app_network
    restart: always

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:

networks:
  app_network:
    driver: bridge
```

## 🛠️ Comandos Útiles

### Desarrollo
```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Reconstruir imágenes
docker-compose build --no-cache

# Detener servicios
docker-compose down

# Eliminar volúmenes (cuidado: pierdes datos)
docker-compose down -v

# Acceder a contenedores
docker-compose exec backend bash
docker-compose exec postgres psql -U postgres -d mi_proyecto_db
docker-compose exec redis redis-cli

# Realizar migraciones
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Recoger archivos estáticos
docker-compose exec backend python manage.py collectstatic --noinput
```

### Producción
```bash
# Usar archivo de producción
docker-compose -f docker-compose.prod.yml up -d

# Escalar servicios
docker-compose -f docker-compose.prod.yml up -d --scale backend=3 --scale celery_worker=2

# Actualizar servicios
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Backup de base de datos
docker-compose exec postgres pg_dump -U postgres mi_proyecto_db > backup.sql

# Restaurar base de datos
docker-compose exec -T postgres psql -U postgres mi_proyecto_db < backup.sql
```

## 🔧 Monitoreo y Debugging

### Health Checks
```bash
# Ver estado de los servicios
docker-compose ps

# Ver recursos utilizados
docker stats

# Ver logs de errores
docker-compose logs backend | grep ERROR
docker-compose logs postgres | grep ERROR
```

### Performance
```bash
# Monitorear PostgreSQL
docker-compose exec postgres psql -U postgres -d mi_proyecto_db -c "
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation 
FROM pg_stats 
WHERE schemaname = 'public';
"

# Monitorear Redis
docker-compose exec redis redis-cli info memory
docker-compose exec redis redis-cli info stats
```

## 🚀 Despliegue

### Local Development
```bash
# Clonar repositorio
git clone <repository-url>
cd mi-proyecto

# Copiar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Iniciar servicios
docker-compose up -d

# Acceder a las aplicaciones
# Frontend: http://localhost
# Backend API: http://localhost:8000/api/
# Admin Django: http://localhost:8000/admin/
# pgAdmin: http://localhost:5050
# Redis Commander: http://localhost:8081
```

### Production Deployment
```bash
# Configurar variables de producción
cp .env.example .env.prod
# Editar .env.prod con valores de producción

# Desplegar en producción
docker-compose -f docker-compose.prod.yml up -d

# Configurar SSL (Let's Encrypt recomendado)
# Actualizar nginx.prod.conf con certificados SSL
```

## 📊 Arquitectura de Microservicios

### ¿Por qué SÍ usar microservicios aquí?

1. **Escalabilidad Independiente**: 
   - Frontend puede escalar separado del backend
   - Celery workers pueden escalar según carga de tareas
   - Base de datos puede tener su propio escalado

2. **Desarrollo Paralelo**:
   - Equipo frontend trabaja independientemente del backend
   - Backend puede tener múltiples equipos (API, workers, etc.)

3. **Tecnologías Específicas**:
   - PostgreSQL para datos relacionales
   - Redis para caching y colas
   - Nginx para serving estático y reverse proxy

### ¿Cuándo NO usar microservicios?

1. **Proyecto Pequeño**: Si es una aplicación simple, monolito es mejor
2. **Equipo Pequeño**: Si tienes 1-2 desarrolladores, microservicios es overkill
3. **Timeline Apretado**: Microservicios requiere más configuración inicial

### Recomendación para tu caso:

**SÍ, implementa microservicios** porque:
- Tienes stack completo (Python + Angular + PostgreSQL)
- Quieres aprender y fortalecer DevOps
- Es un buen proyecto para aprender orquestación
- Te prepara para arquitecturas enterprise

**Pero empieza simple**:
1. Comienza con docker-compose.yml básico
2. Añade servicios gradualmente (Redis, Celery)
3. Evoluciona a Kubernetes cuando domines Docker
```
