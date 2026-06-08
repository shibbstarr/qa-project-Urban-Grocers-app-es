# Proyecto de Pruebas Automatizadas de API - Creación de Kits (Urban Grocers)

Este repositorio aloja la automatización de pruebas para el endpoint de creación de kits personales (`/api/v1/kits`) dentro de la aplicación Urban Grocers. Las pruebas validan de manera exhaustiva el comportamiento del parámetro `name`.

## Estructura del Repositorio

- `configuration.py`: Contiene las URLs del servidor y las rutas a los endpoints.
- `data.py`: Almacena diccionarios y cabeceras base sin procesar lógica.
- `sender_stand_request.py`: Gestiona las peticiones HTTP (`POST`) interactuando con la librería `requests`.
- `create_kit_name_kit_test.py`: Reúne las funciones de aserción y los 9 casos automatizados de la lista de comprobación.

## Requisitos de Ejecución

Asegúrate de contar con Python 3 y de instalar los paquetes requeridos:
```bash
pip install requests pytest