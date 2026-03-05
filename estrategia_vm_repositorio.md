# Estrategia: Local → VM → Repositorio

## 🎯 Flujo de Trabajo Ideal

```
Tu Máquina Local (Solo para documentación)
         ↓
Máquina Virtual (Desarrollo real)
         ↓
Repositorio Git (Control de versiones)
         ↓
Deploy (Producción/Cloud)
```

## 📋 Plan de Acción

### Paso 1: Crear Repositorio Git (Ahora)
```bash
# 1. Crear nuevo repositorio en GitHub
# Nombre: python-angular-postgres-stack
# Descripción: Stack completo Django + Angular + PostgreSQL
# Marcar como Private si quieres

# 2. Clonar en tu máquina local SOLO para estructura inicial
git clone https://github.com/tu-usuario/python-angular-postgres-stack.git
cd python-angular-postgres-stack
```

### Paso 2: Estructura Base del Repositorio
```
python-angular-postgres-stack/
├── README.md
├── .gitignore
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── docs/
│   ├── setup-vm.md
│   ├── arquitectura.md
│   └── deployment.md
├── scripts/
│   ├── setup-vm.sh
│   ├── start-dev.sh
│   └── deploy.sh
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── (estructura Django)
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── (estructura Angular)
└── infrastructure/
    ├── terraform/
    ├── kubernetes/
    └── ansible/
```

## 🚀 Script de Setup para VM

### scripts/setup-vm.sh
```bash
#!/bin/bash

# Setup completo para máquina virtual de desarrollo
echo "🚀 Iniciando setup de entorno de desarrollo..."

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
echo "📦 Instalando Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
echo "📦 Instalando Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Instalar Git
echo "📦 Instalando Git..."
sudo apt install git -y

# Instalar Node.js (para Angular)
echo "📦 Instalando Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar Python y pip
echo "📦 Instalando Python..."
sudo apt install python3 python3-pip python3-venv -y

# Instalar herramientas útiles
echo "📦 Instalando herramientas adicionales..."
sudo apt install htop tree curl wget vim -y

# Crear directorio de trabajo
echo "📁 Creando directorio de proyectos..."
mkdir -p ~/projects
cd ~/projects

# Clonar repositorio
echo "📥 Clonando repositorio del proyecto..."
git clone https://github.com/tu-usuario/python-angular-postgres-stack.git
cd python-angular-postgres-stack

# Copiar variables de entorno
echo "⚙️ Configurando variables de entorno..."
cp .env.example .env

# Dar permisos a scripts
echo "🔐 Configurando permisos..."
chmod +x scripts/*.sh

echo "✅ Setup completado!"
echo ""
echo "📋 Siguientes pasos:"
echo "1. cd ~/projects/python-angular-postgres-stack"
echo "2. Editar .env con tus configuraciones"
echo "3. ./scripts/start-dev.sh"
echo ""
echo "🌐 Accesos:"
echo "- Frontend: http://localhost"
echo "- Backend API: http://localhost:8000/api/"
echo "- Admin Django: http://localhost:8000/admin/"
echo "- pgAdmin: http://localhost:5050"
```

### scripts/start-dev.sh
```bash
#!/bin/bash

echo "🚀 Iniciando entorno de desarrollo..."

# Verificar Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Iniciando..."
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# Verificar archivo .env
if [ ! -f .env ]; then
    echo "❌ Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "⚠️  Por favor edita .env con tus configuraciones"
    exit 1
fi

# Iniciar servicios
echo "🐳 Iniciando contenedores Docker..."
docker-compose up -d

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que PostgreSQL esté listo..."
sleep 10

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones de Django..."
docker-compose exec backend python manage.py migrate

# Recolectar archivos estáticos
echo "📦 Recolectando archivos estáticos..."
docker-compose exec backend python manage.py collectstatic --noinput

# Verificar estado
echo "🔍 Verificando estado de los servicios..."
docker-compose ps

echo ""
echo "✅ Entorno de desarrollo iniciado!"
echo ""
echo "🌐 Servicios disponibles:"
echo "- Frontend (Angular): http://localhost"
echo "- Backend API: http://localhost:8000/api/"
echo "- Admin Django: http://localhost:8000/admin/"
echo "- pgAdmin: http://localhost:5050"
echo "- Redis Commander: http://localhost:8081"
echo ""
echo "📋 Comandos útiles:"
echo "- Ver logs: docker-compose logs -f [servicio]"
echo "- Detener: docker-compose down"
echo "- Reiniciar: docker-compose restart [servicio]"
```

## 📝 .gitignore para el Proyecto

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
.env
.env.local
.env.production

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Node.js/Angular
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
dist/
.angular/
.cache/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
.dockerignore

# Database
*.sql
*.dump

# SSL certificates
*.pem
*.key
*.crt

# Terraform
*.tfstate
*.tfstate.*
.terraform/

# Ansible
*.retry
```

## 🔄 Flujo de Trabajo Completo

### 1. **En tu máquina local (Solo documentación)**
```bash
# 1. Crear repositorio en GitHub
# 2. Clonar SOLO para crear estructura
git clone https://github.com/tu-usuario/python-angular-postgres-stack.git

# 3. Crear archivos base (los que te proporcioné)
# 4. Hacer commit y push inicial
git add .
git commit -m "feat: Initial project structure with Docker setup"
git push origin main
```

### 2. **En tu máquina virtual (Desarrollo real)**
```bash
# 1. Clonar repositorio en VM
git clone https://github.com/tu-usuario/python-angular-postgres-stack.git
cd python-angular-postgres-stack

# 2. Ejecutar script de setup
chmod +x scripts/setup-vm.sh
./scripts/setup-vm.sh

# 3. Iniciar desarrollo
./scripts/start-dev.sh
```

### 3. **Ciclo de Desarrollo**
```bash
# En VM
cd ~/projects/python-angular-postgres-stack

# Hacer cambios en el código
# Probar con docker-compose

# Commits frecuentes
git add .
git commit -m "feat: Add user authentication"
git push origin main

# Desde tu máquina local (solo para revisar)
git pull origin main
# Ver cambios, documentar, etc.
```

## 🛠️ Configuración de SSH para Git

### En tu máquina local
```bash
# Generar SSH key
ssh-keygen -t ed25519 -C "tu-email@example.com"

# Agregar a GitHub
# Settings > SSH and GPG keys > New SSH key
cat ~/.ssh/id_ed25519.pub | clip
```

### En la VM
```bash
# Copiar tu SSH key a la VM
ssh-copy-key user@tu-vm-ip

# O generar nueva key para la VM
ssh-keygen -t ed25519 -C "vm-dev@example.com"
# Agregar también a GitHub
```

## 📋 Checklist de Migración

### ✅ Antes de mover a VM
- [ ] Crear repositorio GitHub
- [ ] Subir estructura base
- [ ] Configurar SSH keys
- [ ] Documentar setup

### ✅ En la VM
- [ ] Instalar prerequisites
- [ ] Clonar repositorio
- [ ] Ejecutar setup script
- [ ] Verificar todos los servicios
- [ ] Probar acceso web

### ✅ Flujo de trabajo
- [ ] Desarrollo en VM
- [ ] Commits regulares
- [ ] Pulls desde local para revisión
- [ ] Documentación actualizada

## 🚀 Comandos de Emergencia

### Si algo falla en VM
```bash
# Limpiar todo
docker-compose down -v
docker system prune -a

# Reinstalar Docker
sudo apt-get purge docker-ce docker-ce-cli containerd.io
sudo apt-get autoremove
sudo apt-get autoclean

# Volver a instalar
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Backup y Restore
```bash
# Backup de base de datos
docker-compose exec postgres pg_dump -U postgres mi_proyecto_db > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres mi_proyecto_db < backup.sql
```

## 📞 Soporte y Troubleshooting

### Problemas Comunes
1. **Permisos de Docker**: `sudo usermod -aG docker $USER`
2. **Puertos ocupados**: `sudo netstat -tulpn | grep :80`
3. **Memoria insuficiente**: `free -h` y `docker stats`
4. **Git permissions**: `git config --global user.name "Tu Nombre"`

### Logs Útiles
```bash
# Logs de Docker
docker-compose logs -f

# Logs específicos
docker-compose logs -f backend
docker-compose logs -f postgres

# Logs del sistema
sudo journalctl -u docker
```

---

## 🎯 Resumen del Plan

1. **Ahora**: Crear repositorio y subir estructura base
2. **Luego**: Configurar VM con script automatizado
3. **Después**: Desarrollo completo en VM
4. **Siempre**: Sincronización con repositorio

**¿Quieres que empecemos a crear el repositorio ahora mismo?** Puedo guiarte paso a paso para crear la estructura perfecta.
