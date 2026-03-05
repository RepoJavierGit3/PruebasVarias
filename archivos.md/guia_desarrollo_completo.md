# Guía Maestra de Desarrollo Full Stack

## 🚀 Stack de Desarrollo Principal

### 1. **.NET Core 8 (Microsoft Ecosystem)**
- **APIs REST**: Web API, Minimal APIs, gRPC
- **Entity Framework Core**: Code First, Database First, Migraciones
- **Arquitectura Limpia**: Clean Architecture, DDD, CQRS
- **Autenticación**: JWT, Identity Server, OAuth 2.0
- **Testing**: xUnit, NUnit, Moq, Integration Tests
- **Performance**: Caching, Async/Await, Memory Optimization

#### Comandos Esenciales .NET 8
```bash
# Crear proyectos
dotnet new webapi -n MiApi --framework net8.0
dotnet new classlib -n MiCore.Domain
dotnet new mvc -n MiWebApp --framework net8.0

# Entity Framework Core
dotnet ef migrations add InitialCreate
dotnet ef database update
dotnet ef dbcontext scaffold "connection-string" Microsoft.EntityFrameworkCore.SqlServer

# Build y Publish
dotnet build -c Release
dotnet publish -c Release -o ./publish
dotnet run --environment Development

# Testing
dotnet test
dotnet test --logger "console;verbosity=detailed"
```

#### Arquitectura .NET 8 Recomendada
```
MiSolucion/
├── src/
│   ├── MiApi.Domain/
│   ├── MiApi.Application/
│   ├── MiApi.Infrastructure/
│   ├── MiApi.API/
│   └── MiApi.Tests/
├── docs/
├── docker/
└── scripts/
```

### 2. **Python & Django (Web Development)**
- **Django Framework**: Models, Views, Templates, Admin
- **Django REST Framework**: APIs, Serializers, Authentication
- **Async Python**: FastAPI, asyncio, performance
- **Data Science**: Pandas, NumPy, Matplotlib
- **Testing**: pytest, Django Test Framework
- **Virtual Environments**: venv, pipenv, poetry

#### Comandos Esenciales Python/Django
```bash
# Entornos virtuales
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Django
django-admin startproject mi_proyecto
python manage.py startapp mi_app
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# FastAPI
pip install fastapi uvicorn
uvicorn mi_app:app --reload

# Testing
pytest
pytest --cov=mi_app
coverage run -m pytest
```

#### Estructura Django Recomendada
```
mi_proyecto/
├── manage.py
├── requirements.txt
├── mi_proyecto/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/
│   ├── users/
│   └── api/
├── static/
├── media/
└── templates/
```

### 3. **Java & Spring Boot (Enterprise Development)**
- **Spring Boot**: REST APIs, Microservicios, Spring Security
- **Spring Data JPA**: Hibernate, Repositories, Query Methods
- **Spring Cloud**: Microservicios, Config Server, Service Discovery
- **Maven/Gradle**: Build Management, Dependencies
- **Testing**: JUnit 5, Mockito, TestContainers
- **Java 17+**: Features, Records, Pattern Matching, Virtual Threads

#### Comandos Esenciales Java/Spring Boot
```bash
# Crear proyecto Spring Boot
spring init --dependencies=web,data-jpa,security,mysql mi-spring-app

# Maven
mvn clean install
mvn spring-boot:run
mvn test

# Gradle
./gradlew build
./gradlew bootRun
./gradlew test

# Docker
docker build -t mi-spring-app .
docker run -p 8080:8080 mi-spring-app
```

#### Estructura Spring Boot Recomendada
```
mi-spring-app/
├── src/
│   ├── main/
│   │   ├── java/com/miapp/
│   │   │   ├── config/
│   │   │   ├── controller/
│   │   │   ├── service/
│   │   │   ├── repository/
│   │   │   ├── model/
│   │   │   └── MiAppApplication.java
│   │   └── resources/
│   │       ├── application.yml
│   │       └── application-dev.yml
│   └── test/
├── pom.xml o build.gradle
└── Dockerfile
```

---

## 🗄️ Bases de Datos y ORM

### SQL Databases
```bash
# SQL Server (con .NET)
"Server=localhost;Database=MiDB;Trusted_Connection=true;"

# PostgreSQL (con Django/Django REST)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mi_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# MySQL (con Spring Boot)
spring.datasource.url=jdbc:mysql://localhost:3306/mi_db
spring.datasource.username=root
spring.datasource.password=password
```

### NoSQL Databases
```bash
# MongoDB (con .NET)
services.AddDbContext<MongoContext>(options =>
    options.UseMongoDatabase(connectionString, "mi_db"));

# Redis (caching)
services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = "localhost:6379";
});
```

---

## 🐳 Docker para Desarrollo

### Dockerfiles Multiplataforma
```dockerfile
# .NET Core 8
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["MiApi.csproj", "."]
RUN dotnet restore "./MiApi.csproj"
COPY . .
WORKDIR "/src/."
RUN dotnet build "MiApi.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "MiApi.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MiApi.dll"]
```

```dockerfile
# Python Django
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```dockerfile
# Java Spring Boot
FROM openjdk:17-jdk-slim

WORKDIR /app

COPY target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Docker Compose para Desarrollo
```yaml
version: '3.8'

services:
  api-net:
    build: ./dotnet-api
    ports:
      - "5000:80"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Server=sql-server;Database=MiDB;User Id=sa;Password=Password123;
    depends_on:
      - sql-server

  api-python:
    build: ./django-api
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/mi_db
    depends_on:
      - postgres

  api-java:
    build: ./spring-boot-api
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=dev
      - SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/mi_db
    depends_on:
      - mysql

  sql-server:
    image: mcr.microsoft.com/mssql/server:2019-latest
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=Password123
    ports:
      - "1433:1433"

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=mi_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"

  mysql:
    image: mysql:8
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=mi_db
    ports:
      - "3306:3306"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

---

## 🧪 Testing Strategies

### .NET Testing
```csharp
// Unit Test con xUnit
public class ProductServiceTests
{
    private readonly IProductService _service;
    private readonly Mock<IProductRepository> _mockRepo;

    public ProductServiceTests()
    {
        _mockRepo = new Mock<IProductRepository>();
        _service = new ProductService(_mockRepo.Object);
    }

    [Fact]
    public async Task GetProductById_ReturnsProduct()
    {
        // Arrange
        var productId = 1;
        var expectedProduct = new Product { Id = productId, Name = "Test Product" };
        _mockRepo.Setup(x => x.GetByIdAsync(productId)).ReturnsAsync(expectedProduct);

        // Act
        var result = await _service.GetProductByIdAsync(productId);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(productId, result.Id);
    }
}
```

### Python Testing
```python
# Django Test
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class ProductAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_product(self):
        data = {
            'name': 'Test Product',
            'price': 99.99,
            'description': 'Test Description'
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
```

### Java Testing
```java
// Spring Boot Test
@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.jpa.hibernate.ddl-auto=create-drop"
})
public class ProductServiceTest {

    @Autowired
    private ProductService productService;

    @MockBean
    private ProductRepository productRepository;

    @Test
    public void whenGetProductById_thenReturnProduct() {
        // Given
        Product product = new Product("Test Product", 99.99);
        when(productRepository.findById(1L)).thenReturn(Optional.of(product));

        // When
        Product found = productService.getProductById(1L);

        // Then
        assertThat(found.getName()).isEqualTo("Test Product");
    }
}
```

---

## 🏗️ Arquitecturas y Patrones

### Microservicios
```csharp
// .NET Core Microservice
[ApiController]
[Route("api/[controller]")]
public class ProductController : ControllerBase
{
    private readonly IProductService _service;
    private readonly ILogger<ProductController> _logger;

    public ProductController(IProductService service, ILogger<ProductController> logger)
    {
        _service = service;
        _logger = logger;
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> GetProduct(int id)
    {
        try
        {
            var product = await _service.GetProductByIdAsync(id);
            return Ok(product);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting product {Id}", id);
            return StatusCode(500, "Internal server error");
        }
    }
}
```

### Clean Architecture
```
src/
├── Domain/           # Entidades, interfaces, value objects
├── Application/      # Use cases, services, DTOs
├── Infrastructure/   # Data access, external services
├── API/             # Controllers, middleware
└── Tests/           # Unit tests, integration tests
```

---

## 🚀 Performance y Optimización

### .NET Performance
```csharp
// Async/Await patterns
public async Task<IEnumerable<ProductDto>> GetProductsAsync()
{
    var products = await _repository.GetAllAsync();
    return products.Select(p => new ProductDto
    {
        Id = p.Id,
        Name = p.Name,
        Price = p.Price
    });
}

// Caching
[ResponseCache(Duration = 60)]
public async Task<ActionResult<ProductDto>> GetProduct(int id)
{
    var product = await _cache.GetOrCreateAsync($"product_{id}", async entry =>
    {
        entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);
        return await _service.GetProductByIdAsync(id);
    });
    
    return Ok(product);
}
```

### Python Performance
```python
# Async Django Views
from django.http import JsonResponse
from asgiref.sync import sync_to_async

@sync_to_async
def get_product_async(product_id):
    return Product.objects.get(id=product_id)

async def product_detail(request, product_id):
    product = await get_product_async(product_id)
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'price': product.price
    })
```

### Java Performance
```java
// Reactive Spring Boot
@GetMapping("/products")
public Flux<Product> getAllProducts() {
    return productService.getAllProducts()
        .delayElements(Duration.ofMillis(100));
}

// Caching with Redis
@Cacheable(value = "products", key = "#id")
public Product getProductById(Long id) {
    return productRepository.findById(id)
        .orElseThrow(() -> new ProductNotFoundException(id));
}
```

---

## 🔧 Herramientas de Desarrollo

### IDEs y Editores
- **Visual Studio 2022**: .NET development
- **JetBrains Rider**: Cross-platform .NET
- **PyCharm**: Python development
- **IntelliJ IDEA**: Java development
- **VS Code**: Lightweight, multi-language

### Extensions y Plugins
```json
// VS Code extensions recomendados
{
    "recommendations": [
        "ms-dotnettools.csharp",
        "ms-python.python",
        "ms-python.django",
        "redhat.java",
        "ms-vscode.vscode-json",
        "bradlc.vscode-tailwindcss",
        "ms-vscode.docker"
    ]
}
```

---

## 📋 Checklist de Desarrollo

### Para Cada Proyecto
- [ ] **Setup inicial**: Estructura de carpetas, git init
- [ ] **Dependencies**: paquetes necesarios instalados
- [ ] **Database**: conexión configurada
- [ ] **Testing**: framework de testing configurado
- [ ] **Docker**: Dockerfile y docker-compose
- [ ] **Documentation**: README actualizado

### Buenas Prácticas
- [ ] **Code style**: Consistente en todo el proyecto
- [ ] **Commits**: Mensajes descriptivos y atómicos
- [ ] **Branch strategy**: Feature branches, main protection
- [ ] **Code review**: Pull requests obligatorios
- [ ] **CI/CD**: Build y test automatizados

---

## 🎯 Próximos Pasos

1. **Elegir tu stack principal** para especializarte
2. **Crear proyecto base** con estructura recomendada
3. **Configurar entorno de desarrollo**
4. **Implementar CI/CD básico**
5. **Añadir testing y monitoring**

**¿Con qué tecnología te gustaría empezar a profundizar primero?** .NET Core 8, Python/Django, o Java/Spring Boot?
