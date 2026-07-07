# qa-project-Urban-Grocers-app-es


# Proyecto Urban Routes Automatización - Sprint 9

## Descripción del Proyecto
Este proyecto consiste en la creación de una suite de pruebas automatizadas de extremo a extremo (E2E) para la aplicación web **Urban Routes**. El script cubre completamente el flujo de usuario desde el ingreso de las direcciones de origen y destino, la configuración de tarifas específicas, el registro telefónico mediante la interceptación de códigos SMS simulados, la vinculación de tarjetas de crédito con control de enfoque del teclado, la selección de extras (manta y helados), hasta el procesamiento de la orden y la asignación del conductor.

## Tecnologías y Técnicas Utilizadas
- **Python**: Lenguaje de programación base.
- **Selenium WebDriver**: Framework para la automatización e interacción con el navegador web.
- **Pytest**: Framework de pruebas para estructurar las aserciones y la ejecución de la suite.
- **Page Object Model (POM)**: Patrón de diseño de software utilizado para desacoplar la lógica de las pruebas de los selectores HTML de la interfaz, mejorando la mantenibilidad del código.
- **Esperas Explícitas (WebDriverWait)**: Técnica para mitigar flujos asíncronos y asegurar la estabilidad de la prueba frente a retrasos de renderizado en el backend.

## Instrucciones para Ejecutar las Pruebas
1. Clona el repositorio de manera local dentro de tu entorno de trabajo.
2. Asegúrate de configurar la URL de tu servidor activo dentro de las variables del archivo `data.py`.
3. Instala las dependencias necesarias mediante la terminal de PyCharm:
   ```bash
   pip install selenium pytest