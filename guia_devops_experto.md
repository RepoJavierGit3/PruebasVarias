# Guía Maestra de DevOps - Levantamientos Completos

## 🚀 Stack DevOps Principal

### 1. **Kubernetes (Orquestación de Contenedores)**
- **Clusters**: EKS, AKS, GKE, On-premise
- **Workloads**: Pods, Deployments, StatefulSets, DaemonSets
- **Networking**: Services, Ingress, Network Policies
- **Storage**: PersistentVolumes, StorageClasses
- **Security**: RBAC, Secrets, Network Policies
- **Monitoring**: Prometheus, Grafana, AlertManager

#### Comandos Esenciales Kubernetes
```bash
# Cluster Management
kubectl cluster-info
kubectl get nodes
kubectl top nodes

# Pods y Deployments
kubectl get pods -A
kubectl get deployments
kubectl describe pod <pod-name>
kubectl logs <pod-name> -f

# Services y Networking
kubectl get services
kubectl get ingress
kubectl port-forward service/<service-name> 8080:80

# Configuración
kubectl apply -f deployment.yaml
kubectl delete deployment <deployment-name>
kubectl edit deployment <deployment-name>

# Troubleshooting
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl exec -it <pod-name> -- /bin/bash
kubectl get all -n <namespace>
```

#### Manifiestos Kubernetes
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mi-api-deployment
  labels:
    app: mi-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mi-api
  template:
    metadata:
      labels:
        app: mi-api
    spec:
      containers:
      - name: mi-api
        image: mi-registry/mi-api:v1.0.0
        ports:
        - containerPort: 80
        env:
        - name: ASPNETCORE_ENVIRONMENT
          value: "Production"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: mi-api-service
spec:
  selector:
    app: mi-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mi-api-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.midominio.com
    secretName: api-tls
  rules:
  - host: api.midominio.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mi-api-service
            port:
              number: 80
```

### 2. **Terraform (Infraestructura como Código)**
- **Providers**: AWS, Azure, GCP, Kubernetes
- **Modules**: Reutilizables y parametrizables
- **State Management**: Remote state, state locking
- **Workspaces**: Multi-environment deployments
- **Testing**: Terratest, validate, plan

#### Comandos Esenciales Terraform
```bash
# Inicialización
terraform init
terraform init -upgrade

# Plan y Apply
terraform plan
terraform plan -out=tfplan
terraform apply tfplan
terraform apply -auto-approve

# State Management
terraform state list
terraform state show <resource>
terraform state mv <source> <destination>
terraform state rm <resource>

# Formateo y Validación
terraform fmt
terraform validate
terraform fmt -recursive

# Workspaces
terraform workspace new development
terraform workspace select production
terraform workspace list

# Destroy
terraform destroy
terraform destroy -auto-approve
```

#### Estructura Terraform Recomendada
```
terraform/
├── environments/
│   ├── development/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks-cluster/
│   ├── rds/
│   └── s3/
├── global/
│   ├── iam/
│   └── security/
└── backend.tf
```

#### Terraform Module Example
```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-vpc"
    }
  )
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  map_public_ip_on_launch = true

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-public-subnet-${count.index + 1}"
      Type = "Public"
    }
  )
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-igw"
    }
  )
}

# modules/vpc/variables.tf
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}
```

### 3. **Ansible (Automatización y Configuración)**
- **Playbooks**: YAML configuration files
- **Roles**: Reusable configuration units
- **Inventory**: Target hosts management
- **Modules**: Pre-built automation tasks
- **Vault**: Encrypted variables

#### Comandos Esenciales Ansible
```bash
# Ejecutar Playbooks
ansible-playbook -i inventory playbook.yml
ansible-playbook -i inventory playbook.yml --check
ansible-playbook -i inventory playbook.yml --diff

# Ad-hoc Commands
ansible all -i inventory -m ping
ansible webservers -i inventory -m apt -a "name=nginx state=present"
ansible webservers -i inventory -m service -a "name=nginx state=started"

# Vault
ansible-vault create secrets.yml
ansible-vault edit secrets.yml
ansible-vault view secrets.yml
ansible-playbook --ask-vault-pass playbook.yml

# Galaxy (roles)
ansible-galaxy install geerlingguy.docker
ansible-galaxy init mi-role
```

#### Ansible Playbook Example
```yaml
# site.yml
---
- name: Setup Web Servers
  hosts: webservers
  become: yes
  vars_files:
    - vars/secrets.yml
    - vars/config.yml

  roles:
    - common
    - docker
    - nginx
    - nodejs

  tasks:
    - name: Ensure application directory exists
      file:
        path: /opt/myapp
        state: directory
        mode: '0755'
        owner: www-data
        group: www-data

    - name: Deploy application
      git:
        repo: 'https://github.com/mi-org/mi-app.git'
        dest: /opt/myapp
        version: main
        force: yes
      notify: restart nginx

    - name: Install application dependencies
      npm:
        path: /opt/myapp
        state: present

  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted

---
- name: Setup Database Servers
  hosts: databases
  become: yes
  roles:
    - postgresql
```

### 4. **GitHub & GitHub Actions (CI/CD)**
- **Repositories**: Branch protection, PR templates
- **Actions**: Workflows, runners, secrets
- **Packages**: Container registry, npm registry
- **Security**: Code scanning, dependabot, secret scanning

#### GitHub Actions Workflows
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        dotnet-version: ['8.0.x']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup .NET
      uses: actions/setup-dotnet@v3
      with:
        dotnet-version: ${{ matrix.dotnet-version }}
    
    - name: Restore dependencies
      run: dotnet restore
    
    - name: Build
      run: dotnet build --no-restore
    
    - name: Test
      run: dotnet test --no-build --verbosity normal
    
    - name: Code Coverage
      run: dotnet test --no-build --verbosity normal --collect:"XPlat Code Coverage"
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build-and-push:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Update kubeconfig
      run: aws eks update-kubeconfig --name staging-cluster
    
    - name: Deploy to staging
      run: |
        helm upgrade --install mi-app ./helm-chart \
          --namespace staging \
          --create-namespace \
          --set image.tag=${{ github.sha }} \
          --set environment=staging

  deploy-production:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Update kubeconfig
      run: aws eks update-kubeconfig --name production-cluster
    
    - name: Deploy to production
      run: |
        helm upgrade --install mi-app ./helm-chart \
          --namespace production \
          --create-namespace \
          --set image.tag=${{ github.sha }} \
          --set environment=production
```

### 5. **ArgoCD (GitOps)**
- **Applications**: Kubernetes deployment management
- **Sync**: Automated and manual sync strategies
- **Rollback**: Version control for deployments
- **Multi-cluster**: Managing multiple clusters
- **App of Apps**: Pattern for managing multiple applications

#### ArgoCD Application Example
```yaml
# argocd-apps/mi-api-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: mi-api-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/mi-org/mi-k8s-manifests.git
    targetRevision: HEAD
    path: environments/production/mi-api
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 3

---
# ApplicationSet para múltiples entornos
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: mi-api-appset
  namespace: argocd
spec:
  generators:
  - git:
      repoURL: https://github.com/mi-org/mi-k8s-manifests.git
      revision: HEAD
      directories:
      - path: environments/*
  template:
    metadata:
      name: 'mi-api-{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/mi-org/mi-k8s-manifests.git
        targetRevision: HEAD
        path: '{{path}}/mi-api'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### 6. **Terrabit (IaC Testing)**
- **Testing**: Unit tests para Terraform
- **Validation**: Pre-deployment verification
- **Compliance**: Policy as code
- **Documentation**: Automated docs generation

#### Terratest Example
```go
// test/mi_vpc_test.go
package test

import (
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/aws"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestVPC(t *testing.T) {
	t.Parallel()

	// Configuración de Terraform
	terraformOptions := &terraform.Options{
		TerraformDir: "../modules/vpc",
		Vars: map[string]interface{}{
			"project_name": "test-project",
			"vpc_cidr":     "10.0.0.0/16",
		},
	}

	// Cleanup al finalizar
	defer terraform.Destroy(t, terraformOptions)

	// Init y Apply
	terraform.InitAndApply(t, terraformOptions)

	// Obtener outputs
	vpcID := terraform.Output(t, terraformOptions, "vpc_id")
	publicSubnetIDs := terraform.OutputList(t, terraformOptions, "public_subnet_ids")

	// Validaciones
	assert.NotEmpty(t, vpcID)
	assert.Equal(t, 3, len(publicSubnetIDs))

	// Validar VPC en AWS
	vpc := aws.GetVpcById(t, vpcID, "us-east-1")
	assert.Equal(t, "10.0.0.0/16", vpc.CidrBlock)

	// Validar subnets
	for _, subnetID := range publicSubnetIDs {
		subnet := aws.GetSubnetById(t, subnetID, "us-east-1")
		assert.True(t, subnet.MapPublicIpOnLaunch)
		assert.Equal(t, vpcID, subnet.VpcId)
	}
}

func TestVPCWithInvalidCIDR(t *testing.T) {
	t.Parallel()

	terraformOptions := &terraform.Options{
		TerraformDir: "../modules/vpc",
		Vars: map[string]interface{}{
			"project_name": "test-project",
			"vpc_cidr":     "invalid-cidr",
		},
	}

	// Validar que falle con CIDR inválido
	_, err := terraform.InitAndApplyE(t, terraformOptions)
	assert.Error(t, err)
}
```

---

## 🏗️ Levantamientos Completos - End-to-End

### Escenario 1: Microservicios .NET Core en EKS
```hcl
# main.tf - Infraestructura completa
module "vpc" {
  source = "./modules/vpc"
  
  project_name = "mi-plataforma"
  environment  = "production"
  vpc_cidr     = "10.0.0.0/16"
}

module "eks_cluster" {
  source = "./modules/eks-cluster"
  
  project_name = "mi-plataforma"
  environment  = "production"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  
  node_groups = {
    general = {
      instance_type = "m5.large"
      min_size     = 2
      max_size     = 10
      desired_size = 3
    }
    system = {
      instance_type = "m5.medium"
      min_size     = 1
      max_size     = 3
      desired_size = 1
    }
  }
}

module "rds" {
  source = "./modules/rds"
  
  project_name = "mi-plataforma"
  environment  = "production"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  
  engine         = "postgres"
  engine_version = "15"
  instance_class = "db.m5.large"
  
  database_name = "mi_plataforma"
  username      = "postgres"
  
  skip_final_snapshot = false
}

module "elasticache" {
  source = "./modules/elasticache"
  
  project_name = "mi-plataforma"
  environment  = "production"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  
  node_type = "cache.m5.large"
  num_cache_nodes = 2
}
```

### Escenario 2: CI/CD Pipeline Completo
```yaml
# .github/workflows/complete-pipeline.yml
name: Complete DevOps Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup .NET
      uses: actions/setup-dotnet@v3
      with:
        dotnet-version: '8.0.x'
    
    - name: Restore dependencies
      run: dotnet restore
    
    - name: Code formatting check
      run: dotnet format --verify-no-changes
    
    - name: Static analysis
      run: dotnet tool run dotnet-sonarscanner begin /k:"mi-proyecto" /d:sonar.login="${{ secrets.SONAR_TOKEN }}"
    
    - name: Build
      run: dotnet build --no-restore
    
    - name: Test
      run: dotnet test --no-build --verbosity normal --collect:"XPlat Code Coverage"
    
    - name: SonarCloud analysis
      run: dotnet tool run dotnet-sonarscanner end /d:sonar.login="${{ secrets.SONAR_TOKEN }}"

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Snyk to check for vulnerabilities
      uses: snyk/actions/dotnet@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
    
    - name: OWASP Dependency Check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: 'mi-proyecto'
        path: '.'
        format: 'HTML'
    
    - name: Upload OWASP results
      uses: actions/upload-artifact@v3
      with:
        name: owasp-report
        path: reports/

  infrastructure-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
      with:
        terraform_version: "1.5.0"
    
    - name: Terraform Format Check
      run: terraform fmt -check -recursive
    
    - name: Terraform Init
      run: terraform init -backend-config="bucket=${{ secrets.TF_STATE_BUCKET }}"
    
    - name: Terraform Validate
      run: terraform validate
    
    - name: Terraform Plan
      run: terraform plan -out=tfplan
    
    - name: Terratest
      run: |
        cd test
        go mod tidy
        go test -v -timeout 30m

  build-and-deploy:
    needs: [code-quality, security-scan, infrastructure-test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Login to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          ghcr.io/${{ github.repository }}:latest
          ghcr.io/${{ github.repository }}:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Deploy to Kubernetes
      run: |
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig
        
        # Update image tag in deployment
        kubectl set image deployment/mi-api mi-api=ghcr.io/${{ github.repository }}:${{ github.sha }} -n production
        
        # Wait for rollout
        kubectl rollout status deployment/mi-api -n production
        
        # Verify deployment
        kubectl get pods -n production
```

---

## 🔧 Herramientas DevOps Esenciales

### Monitoring y Observability
```yaml
# prometheus-config.yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
    - role: pod
    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true

  - job_name: 'mi-api-metrics'
    static_configs:
    - targets: ['mi-api-service:80']
    metrics_path: /metrics
    scrape_interval: 10s
```

### Logging con ELK Stack
```yaml
# elasticsearch.yml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
spec:
  serviceName: elasticsearch
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
        env:
        - name: discovery.type
          value: single-node
        - name: ES_JAVA_OPTS
          value: "-Xms512m -Xmx512m"
        ports:
        - containerPort: 9200
          name: http
        volumeMounts:
        - name: data
          mountPath: /usr/share/elasticsearch/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

---

## 📋 Checklist de Levantamientos

### Infraestructura
- [ ] **VPC y Networking**: Subnets, Route Tables, Security Groups
- [ ] **Compute**: EC2, EKS, Lambda configurados
- [ ] **Storage**: S3, EBS, RDS aprovisionados
- [ ] **Security**: IAM roles, policies, encryption
- [ ] **Monitoring**: CloudWatch, Prometheus, alerts

### Aplicaciones
- [ ] **Containers**: Docker images optimizados
- [ ] **Kubernetes**: Deployments, Services, Ingress
- [ ] **Configuration**: Secrets, ConfigMaps
- [ ] **Health Checks**: Liveness, readiness probes
- [ ] **Scaling**: HPA, VPA configurados

### CI/CD
- [ ] **Source Control**: Branch protection, PR templates
- [ ] **Build Pipeline**: Test, security scan, build
- [ ] **Deployment Pipeline**: Staging, production gates
- [ ] **Rollback**: Automated rollback strategies
- [ ] **Notifications**: Slack, email alerts

### Monitoring
- [ ] **Metrics**: Application, infrastructure metrics
- [ ] **Logging**: Centralized logging setup
- [ ] **Alerting**: Critical alerts configured
- [ ] **Dashboards**: Grafana dashboards
- [ ] **Health Checks**: Endpoints monitoring

---

## 🎯 Proyectos de Práctica

### 1. **Microservicios E-commerce**
- .NET Core API Products
- Python Orders Service
- Java Payment Service
- React Frontend
- PostgreSQL databases
- Redis caching

### 2. **SaaS Platform**
- Multi-tenant architecture
- Kubernetes deployment
- Terraform infrastructure
- CI/CD pipeline
- Monitoring stack
- Security scanning

### 3. **Data Processing Pipeline**
- Lambda functions
- Kinesis streams
- S3 storage
- Glue jobs
- Athena queries
- QuickSight dashboards

---

## 🚀 Roadmap de Aprendizaje

### Nivel 1: Fundamentos (1-2 meses)
- Docker y Kubernetes básico
- Terraform fundamentals
- GitHub Actions básico
- AWS/Azure services básicos

### Nivel 2: Intermedio (2-3 meses)
- Kubernetes avanzado
- Terraform modules
- CI/CD pipelines complejos
- Monitoring y logging

### Nivel 3: Avanzado (3-4 meses)
- Multi-cloud deployments
- GitOps con ArgoCD
- Security DevOps
- Performance optimization

### Nivel 4: Experto (4-6 meses)
- Large scale deployments
- Cost optimization
- Compliance y governance
- Team leadership DevOps

**¿Con qué tecnología te gustaría empezar a profundizar primero?** Kubernetes, Terraform, o CI/CD pipelines?
