# Sistema de Automatización RPA - Registro de Usuarios

Juan Jose Velez Orozco

### Componentes del Sistema

#### Generador de Credenciales (`generador_credenciales.py`)
Módulo encargado de generar datos de usuarios ficticios. Utiliza la librería Faker para crear información realista que incluye nombres, correos electrónicos, contraseñas seguras, direcciones y números telefónicos. Los datos generados siguen patrones consistentes para garantizar la validez en formularios web.

#### Archivo de Configuración (`config.json`)
Archivo formato JSON que almacena las credenciales de usuarios generadas. Este archivo actúa como fuente de datos para el módulo de registro, manteniendo la información estructurada y accesible para su posterior procesamiento automatizado.

#### Módulo de Registro (`registro_usuarios.py`)
Componente de automatización que utiliza Selenium para ejecutar el registro de usuarios en automationexercise.com. Lee las credenciales del archivo config.json y completa automáticamente los formularios de registro web, simulando la interacción humana con la interfaz.

## Funcionalidad Principal

El sistema automatiza el proceso completo de registro de 5 usuarios:
- Generación de datos de usuarios ficticios
- Navegación automatizada a la página de registro
- Completado automático de formularios web
- Validación y confirmación de registros exitosos

## Instalación y Configuración

### Requisitos Previos
- Python 3.11.0
- Navegador web compatible con Selenium (Chrome recomendado)
- ChromeDriver para automatización web

### Configuración del Entorno

1. **Crear ambiente virtual:**
   ```bash
   python -m venv venv
   ```

2. **Activar el ambiente virtual:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install faker selenium
   ```

## Ejecución del Sistema

### Paso 1: Generar Credenciales
```bash
python generador_credenciales.py
```
Genera 5 usuarios ficticios y los almacena en `config.json`

### Paso 2: Ejecutar Automatización de Registro
```bash
python registro_usuarios.py
```
Ejecuta el proceso automatizado de registro en automationexercise.com

## Estructura del Proyecto

```
proyecto/
├── generador_credenciales.py    # Generación de datos ficticios
├── registro_usuarios.py         # Automatización Selenium
├── config.json                  # Datos de usuarios generados
├── venv/                        # Entorno virtual Python
└── README.md                    # Documentación
```

## Especificaciones Técnicas

- **Librería de datos ficticios:** Faker
- **Framework de automatización:** Selenium WebDriver
- **Formato de almacenamiento:** JSON
- **Navegador objetivo:** automationexercise.com
- **Cantidad de registros:** 5 usuarios por ejecución
