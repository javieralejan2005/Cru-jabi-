# crupython

Proyecto de ejemplo para implementar operaciones CRUD (Create, Read, Update, Delete) en Python. Sirve como plantilla educativa para aprender patrones básicos de persistencia, diseño de API y pruebas mínimas.

## Descripción
Crupython contiene código y ejemplos para gestionar una entidad (por ejemplo: usuarios, tareas o productos) mediante operaciones CRUD. Está pensado para ser simple, extensible y fácil de adaptar a diferentes almacenamientos (SQLite, archivos JSON o bases de datos relacionales).

## Características
- Operaciones básicas: crear, listar, leer, actualizar y eliminar registros.
- Persistencia ligera (ejemplo con SQLite / JSON).
- Endpoints REST simples (opcional, ejemplo con Flask/FastAPI).
- Tests básicos para las operaciones CRUD.
- Script de inicialización y ejemplos de uso.

## Tecnologías
- Python 3.8+
- SQLite (o alternativa ligera)
- Opcional: Flask o FastAPI para API REST
- Pytest para pruebas

## Requisitos
- Python 3.8 o superior
- pip

## Instalación
1. Clonar el repositorio:
    ```bash
    git clone <repositorio>
    cd crupython
    ```
2. Crear entorno virtual e instalar dependencias:
    ```bash
    python -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Uso
- Inicializar la base de datos (si aplica):
  ```bash
  python scripts/init_db.py
  ```
- Ejecutar la aplicación (ejemplo Flask):
  ```bash
  export FLASK_APP=app.py
  flask run
  ```
- Ejemplo de uso con curl:
  ```bash
  # Crear
  curl -X POST /items -d '{"name":"ejemplo"}' -H "Content-Type: application/json"
  # Listar
  curl /items
  ```

## Estructura sugerida
- app/               -> Código principal (modelos, rutas, lógica)
- data/              -> Archivo de base de datos o fixtures
- scripts/           -> Utilidades (inicializar DB, migraciones simples)
- tests/             -> Pruebas unitarias
- requirements.txt
- README.md

## Pruebas
Ejecutar tests con:
```bash
pytest
```

## Contribuir
- Abrir issues para bugs o mejoras.
- Enviar pull requests con descripciones claras y tests cuando sea posible.

## Licencia
Proyecto con licencia MIT (o la que prefieras). Añadir archivo LICENSE con los detalles.
