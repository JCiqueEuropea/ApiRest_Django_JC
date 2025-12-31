🎵 Django Spotify Manager API
==============================

![alt text](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white) ![Django-4.2+](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-REST-red?style=for-the-badge)

![alt text](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white) ![alt text](https://img.shields.io/badge/Tests-Pytest-yellow?style=for-the-badge)

Una API RESTful moderna y asíncrona construida con **Django** y **Django Rest Framework (DRF)** que actúa como intermediario inteligente entre tus
usuarios
y la **API de Spotify**. Permite gestionar perfiles de usuarios locales, autenticarse vía OAuth2 con Spotify, buscar
música y gestionar favoritos y seguidos en tiempo real.

🚀 Características Principales
------------------------------

* **Gestión de Usuarios (CRUD):** Creación, lectura, actualización y borrado de usuarios con validaciones estrictas (
  edad,
  formato de nombres, etc.).
* **Integración Spotify OAuth2:** Flujo completo de autenticación (Authorization Code Flow) para actuar en nombre del
  usuario.
* **Búsqueda Asíncrona:** Consultas de Artistas y Canciones utilizando httpx para alto rendimiento.
* **Favoritos:** Guardado de Artistas y Canciones favoritas en el perfil del usuario (con persistencia de metadatos de
  Spotify).
* **Funcionalidad Social:** Endpoint para Seguir (Follow) artistas o usuarios en Spotify y verificar el estado de
  seguimiento.
* **Arquitectura Limpia:** Separación por capas (Views, Services, Models, Domain).
* **Manejo de Errores Robusto:** Respuestas HTTP estandarizadas y mensajes de error descriptivos.

🛠️ Stack Tecnológico
---------------------

* **Framework:** Django 4.2 + Django Rest Framework
* **Validación de Datos:** Django Validators + Pydantic (DTOs)
* **Cliente HTTP:** Httpx
* **Base de Datos:** Microsoft SQL Server (mssql-django + pyodbc)
* **Configuración:** django-environ (.env)


📦 Estructura del Proyecto
---------------------
El proyecto sigue una arquitectura modular para facilitar la escalabilidad:

```
.
├── ApiRest_Django_JC
│   ├── asgi           # Configuración ASGI para despliegues asíncronos y servidores compatibles
│   ├── settings       # Configuración global del proyecto Django (entornos, apps, BD, middleware)
│   ├── urls           # Enrutado principal de URLs del proyecto
│   └── wsgi.py        # Punto de entrada WSGI para servidores de producción
├── app
│   ├── api            # Vistas de la API REST (DRF Views / ViewSets)
│   ├── migrations     # Migraciones de base de datos generadas por Django ORM
│   ├── models         # Modelos de dominio y esquemas Pydantic (DTOs)
│   ├── services       # Lógica de negocio desacoplada de la capa HTTP
│   ├── spotify        # Cliente Spotify, OAuth2 y lógica de integración externa
│   ├── errors.py      # Excepciones personalizadas de la aplicación
│   ├── models.py      # Archivo puente para que Django detecte todos los modelos del paquete app.models
│   └── utils.py       # Utilidades comunes (helpers, validaciones, manejo de errores)
├── tests              # Tests unitarios y de integración
├── .env               # Variables de entorno (No subir al repo)
├── .gitignore
├── manage.py          # Punto de entrada y gestor de comandos Django
├── pytest.ini         # Configuración de pytest para el entorno Django
├── README.md          
└── requirements.txt   # Dependencias de la aplicación
```

⚙️ Instalación y Configuración
------------------------------

### 1\. Prerrequisitos

* Python 3.10 o superior.
* Una cuenta de [Spotify for Developers](https://www.google.com/url?sa=E&q=https://developer.spotify.com/dashboard).

### 2\. Clonar el repositorio

```
git clone https://github.com/tu-usuario/ApiRest_Django_JC.git
cd ApiRest_Django_JC
```

### 3\. Crear entorno virtual

```
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate  
```

### 4\. Instalar dependencias

```
pip install -r requirements.txt
```

### 5\. Configurar Spotify Dashboard

1. Ve a tu Dashboard de Spotify y crea una App.
2. Obtén el **Client ID** y **Client Secret**.
3. En "Edit Settings", añade la siguiente **Redirect URI**:

**Importante:** Debe ser exacta, `localhost` puede dar problemas con cookies.

```
http://127.0.0.1:8000/users/auth/callback
```

### 6\. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

``` 
API_KEY_SECRET="pega_tu_api_key_aqui"
DB_NAME="pega_tu_db_name_aqui"
DB_HOST="pega_tu_db_host_aqui"
ENVIRONMENT="development"
LOG_LEVEL="INFO"
SPOTIFY_CLIENT_ID="pega_tu_client_id_aqui"
SPOTIFY_CLIENT_SECRET="pega_tu_client_secret_aqui"
SPOTIFY_REDIRECT_URI="http://127.0.0.1:8000/users/auth/callback"
```

### 7. Crear y aplicar migraciones de base de datos

Django utiliza un sistema de migraciones propio para versionar el esquema de la base de datos (equivalente a Alembic en SQLAlchemy).

**Crear los archivos de migración a partir de los modelos Django:**

```
python manage.py makemigrations app
```

Este comando analiza los modelos definidos en `app/models/` y genera los archivos de migración en `app/migrations/`
(ej. `0001_initial.py`).

**Aplicar las migraciones a la base de datos:**

```
python manage.py migrate
```

Este comando crea las tablas y restricciones en la base de datos SQL Server según las migraciones generadas.


▶️ Ejecución
------------

Levanta el servidor de desarrollo:

```
python manage.py migrate
python manage.py runserver
```

La API estará disponible en: http://127.0.0.1:8000

📖 Documentación de la API
--------------------------

La API expone documentación OpenAPI mediante DRF Spectacular:

* **Swagger UI:** [http://127.0.0.1:8000/docs](https://www.google.com/url?sa=E&q=http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](https://www.google.com/url?sa=E&q=http://127.0.0.1:8000/redoc)

### Flujo de Uso Básico

1. **Crear Usuario:** `POST/users/`
2. **Login en Spotify:** Abre en el navegador `http://127.0.0.1:8000/spotify/auth/{user_id}/login`.
3. **Autorizar:** Acepta los permisos en Spotify. Serás redirigido y verás un JSON de éxito.
4. **Usar la API:** Usar los endpoints expuestos por DRF para gestionar favoritos y relaciones con Spotify.

🧪 Testing
----------

El proyecto incluye una suite de tests completa usando pytest. Los tests de integración con Spotify utilizan**Mocks**,
por lo que no requieren credenciales reales ni conexión a internet.

Ejecutar tests:

````
pytest -v
````

🛡️ Manejo de Errores
---------------------

La API implementa un manejador global de excepciones mediante DRF y middleware personalizado. Transforma errores de Python en respuestas HTTP JSON
estandarizadas:

* `404 Not Found`: Cuando no existe un usuario o un recurso en Spotify.
* `401 Unauthorized`: Cuando el token de Spotify ha expirado o no existe.
* `422 Validation Error`: Cuando los datos de entrada (edad, nombre) no cumplen las reglas.
* `502 Bad Gateway`: Errores de comunicación con la API externa.

📝 Licencia
-----------

Este proyecto está bajo la Licencia MIT. Siéntete libre de usarlo y modificarlo.
___
Hecho con ❤️ y 🐍 Python para la Universidad Europea