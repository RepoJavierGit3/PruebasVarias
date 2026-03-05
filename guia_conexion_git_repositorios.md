# Guía Completa: Conectar y Gestionar Repositorios Git

## 🔗 Conectar Repositorios Git Existentes

### 1. **Clonar un Repositorio Específico**

#### Método HTTPS (Recomendado para principiantes)
```bash
# Clonar repositorio completo
git clone https://github.com/usuario/nombre-repo.git

# Clonar a carpeta específica
git clone https://github.com/usuario/nombre-repo.git mi-proyecto

# Clonar solo rama específica
git clone --branch main https://github.com/usuario/nombre-repo.git
git clone --single-branch --branch develop https://github.com/usuario/nombre-repo.git
```

#### Método SSH (Más seguro)
```bash
# Generar SSH key (si no tienes)
ssh-keygen -t ed25519 -C "tu-email@example.com"

# Iniciar SSH agent y agregar key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar key pública al portapapeles
cat ~/.ssh/id_ed25519.pub | clip

# Agregar a GitHub: Settings > SSH and GPG keys > New SSH key

# Clonar con SSH
git clone git@github.com:usuario/nombre-repo.git
```

### 2. **Conectar Proyecto Local a Repositorio Remoto**

```bash
# Navegar a tu proyecto local
cd ruta/de/tu/proyecto

# Inicializar Git (si no está inicializado)
git init

# Agregar repositorio remoto
git remote add origin https://github.com/usuario/nombre-repo.git
# O con SSH
git remote add origin git@github.com:usuario/nombre-repo.git

# Verificar conexión
git remote -v

# Hacer pull inicial (si el repo existe)
git pull origin main

# Agregar archivos y hacer commit inicial
git add .
git commit -m "Initial commit"

# Push al repositorio remoto
git push -u origin main
```

### 3. **Trabajar con Repositorios Específicos**

#### Clonar Shallow (solo últimos commits)
```bash
# Clonar solo último commit
git clone --depth 1 https://github.com/usuario/nombre-repo.git

# Clonar últimos N commits
git clone --depth 5 https://github.com/usuario/nombre-repo.git
```

#### Clonar Carpeta Específica (Sparse Checkout)
```bash
# Crear directorio y clonar sin archivos
git clone --no-checkout https://github.com/usuario/nombre-repo.git mi-carpeta
cd mi-carpeta

# Habilitar sparse checkout
git config core.sparsecheckout true

# Especificar carpetas deseadas
echo "src/" > .git/info/sparse-checkout
echo "docs/" >> .git/info/sparse-checkout

# Hacer checkout
git checkout main
```

### 4. **Gestión de Múltiples Repositorios**

#### Verificar Repositorios Remotos
```bash
# Listar todos los remotos
git remote -v

# Ver información de un remoto específico
git remote show origin

# Cambiar URL de remoto
git remote set-url origin https://github.com/nuevo-usuario/nuevo-repo.git
```

#### Trabajar con Múltiples Remotos
```bash
# Agregar segundo remoto (fork)
git remote add fork https://github.com/tu-usuario/nombre-repo.git

# Push a diferentes remotos
git push origin main
git push fork feature-branch

# Pull de diferentes remotos
git pull origin main
git pull fork feature-branch
```

---

## 🛠️ Comandos Esenciales

### Navegación y Estado
```bash
# Ver estado actual
git status

# Ver historial de commits
git log --oneline --graph --all

# Ver cambios en archivos
git diff
git diff --staged
```

### Branch Management
```bash
# Listar branches
git branch -a

# Crear nueva branch
git checkout -b nueva-feature

# Cambiar de branch
git checkout main

# Eliminar branch local
git branch -d feature-terminada

# Eliminar branch remota
git push origin --delete feature-terminada
```

### Sincronización
```bash
# Actualizar información de remotos
git remote update

# Fetch de todos los remotos
git fetch --all

# Pull con rebase (mantiene historial limpio)
git pull --rebase origin main

# Push force (con cuidado)
git push --force-with-lease origin feature-branch
```

---

## 🔐 Autenticación y Configuración

### Configurar Usuario
```bash
# Configurar nombre y email global
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"

# Configurar por repositorio
git config user.name "Tu Nombre"
git config user.email "tu-email@trabajo.com"
```

### GitHub CLI (gh)
```bash
# Instalar GitHub CLI
# Windows: winget install GitHub.cli
# Mac: brew install gh

# Autenticarse
gh auth login

# Clonar repo con gh
gh repo clone usuario/nombre-repo

# Crear nuevo repo
gh repo create mi-nuevo-repo --public --source=. --remote=origin --push
```

### Personal Access Tokens
```bash
# Crear token en GitHub: Settings > Developer settings > Personal access tokens

# Usar token para clonar
git clone https://TOKEN@github.com/usuario/nombre-repo.git

# O configurar en helper
git config --global credential.helper store
# Primera vez te pedirá usuario y token
```

---

## 📁 Estructura Recomendada

### Organización de Proyectos
```
C:\Users\Terminal\Projects\
├── work\
│   ├── api-proyecto-1\
│   ├── frontend-app\
│   └── devops-scripts\
├── personal\
│   ├── mi-blog\
│   └── learning-projects\
└── open-source\
    ├── contribucion-repo\
    └── mi-proyecto-oss
```

### Scripts de Utilidad
```bash
# script: clone-repo.sh
#!/bin/bash
REPO_URL=$1
PROJECT_TYPE=$2
BASE_DIR="C:/Users/Terminal/Projects"

case $PROJECT_TYPE in
    "work")
        TARGET_DIR="$BASE_DIR/work/$(basename $REPO_URL .git)"
        ;;
    "personal")
        TARGET_DIR="$BASE_DIR/personal/$(basename $REPO_URL .git)"
        ;;
    *)
        TARGET_DIR="$BASE_DIR/$(basename $REPO_URL .git)"
        ;;
esac

git clone $REPO_URL $TARGET_DIR
cd $TARGET_DIR
echo "Repositorio clonado en: $TARGET_DIR"
```

---

## 🚀 Flujo de Trabajo Recomendado

### 1. **Inicio del Día**
```bash
# Actualizar repositorio principal
git checkout main
git pull origin main

# Crear nueva feature
git checkout -b feature/nueva-funcionalidad
```

### 2. **Durante Desarrollo**
```bash
# Commits frecuentes y descriptivos
git add .
git commit -m "feat: agregar endpoint de login"

# Mantener actualizado con main
git fetch origin
git rebase origin/main
```

### 3. **Final de Feature**
```bash
# Push de la feature
git push origin feature/nueva-funcionalidad

# Crear Pull Request (con GitHub CLI)
gh pr create --title "Agregar login endpoint" --body "Implementación de autenticación"
```

---

## 🔧 Solución de Problemas Comunes

### Error: "Permission Denied"
```bash
# Verificar SSH key
ssh -T git@github.com

# Regenerar SSH key si es necesario
ssh-keygen -t ed25519 -C "tu-email@example.com"
```

### Error: "Remote Already Exists"
```bash
# Remover remoto existente
git remote remove origin

# Agregar nuevo remoto
git remote add origin https://github.com/usuario/nuevo-repo.git
```

### Merge Conflicts
```bash
# Ver archivos en conflicto
git status

# Resolver conflictos manualmente

# Agregar archivos resueltos
git add archivo-resuelto.cs

# Continuar con rebase o merge
git rebase --continue
# o
git merge --continue
```

---

## 📋 Checklist de Conexión

### Antes de Empezar
- [ ] Git instalado y configurado
- [ ] SSH key generada y agregada a GitHub
- [ ] GitHub CLI instalado (opcional)
- [ ] Directorio de proyectos organizado

### Para Cada Repositorio
- [ ] URL correcta del repositorio
- [ ] Permisos de acceso
- [ ] Branch correcta identificada
- [ ] Estrategia de sincronización definida

### Buenas Prácticas
- [ ] Usar `.gitignore` apropiado
- [ ] Commits atómicos y descriptivos
- [ ] Branch strategy definida
- [ ] Code review antes de merge

---

## 🎯 Ejemplo Práctico Completo

### Escenario: Conectar proyecto .NET Core existente a GitHub

```bash
# 1. Navegar al proyecto
cd C:\Users\Terminal\Projects\mi-api-core

# 2. Inicializar Git
git init

# 3. Crear .gitignore para .NET
echo "bin/
obj/
*.user
*.suo
*.cache
*.dll
*.exe
*.pdb
appsettings.Development.json
" > .gitignore

# 4. Agregar archivos iniciales
git add .
git commit -m "feat: initial .NET Core API structure"

# 5. Crear repositorio en GitHub (via web o CLI)
gh repo create mi-api-core --public --source=. --remote=origin --push

# 6. Configurar upstream
git branch --set-upstream-to=origin/main main

# 7. Verificar conexión
git remote -v
git status
```

**¿Qué tipo de repositorio quieres conectar?** ¿Tienes un proyecto local que quieres subir a GitHub, o quieres clonar un repositorio existente?
