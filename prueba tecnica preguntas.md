**Prueba técnica Desarrollador junior RPA**

**1. Responda con sus palabras las siguientes preguntas con respecto a una automatización:**

**¿Para qué sirve un archivo config?**

Un archivo config sirve para parametrizar, y en ciertos casos orquestar el código, usar un archivo config sirve para tener buenas prácticas, ya que nos ayuda a que el mantenimiento, escalamiento o administración del código u automatización sea más rápido, sencillo y flexible, usualmente se ponen datos que cambian, pueden cambiar para que no toque ir a todas las partes del código donde se llaman a estas variables, sino que directamente se cambian desde un mismo archivo, evitando editar el código, incluso haciéndolo sencillo para personas no técnicas, y también variables que se cambian para pruebas y despliegues.

Un ejemplo es un archivo config con las variables que apuntan a unas tablas en la base de datos, para pruebas se usan ciertas tablas, pero para producción son otras, y es sencillo editarlas desde acá mismo.

**¿Qué extensión(es) o formato(s) usaría para el(los) archivo(s) config?** 

Personalmente uso el formato .JSON, aunque también se podría usar .ENV y/o YAML 

**¿Por que usaría esa(s) extensión(es) o formato(s)?**

Uso el .JSON ya que permite hacer estructuras fáciles y claras, es fácil de usar con código, también fácil de entender para personas no técnicas y en mi trabajo pasado era un estándar usar el archivo config, en JSON (config.json).

El .ENV lo uso para credenciales o variables privadas, información que no puede estar en código o no se puede filtrar.

Y .YAML lo usaría porque a personas no técnicas se les hace fácil de entender y se pueden hacer configuraciones complejas.

Pese a que prefiero el formato .JSON para las automatizaciones, puede variar dependiendo de lo que se requiera.

**¿Qué datos almacenaría en el(los) archivo(s) config?**

- Urls.
- Variables.
- Parámetros
- Tablas que apuntan a la base de datos.
- Querys.
- Rutas de dirección (para logs, descargas, etc).
- Timeouts o delays.
- Configuración de navegador (si es una automatización web con web scraping o similar).
- Horarios de ejecución.
- Credenciales de acceso (en archivo .env separado).

2. **Escriba con sus palabras que excepciones consideraría al automatizar la descarga de archivos de una página web y explique brevemente cada una.**


- Timeouts de conexion: Aveces la pagina se carga mal, o no responde y es bueno poner excepciones. (y también se ponen números de reintentos)
- Captcha o verificación humana: Cuando el sitio implementa medidas anti-bot (acá toca hacer otro tipo de codigo para pasar las pruebas)
- Conexión rechazada: Cuando el servidor rechaza la conexión.
- Archivo no encontrado: Cuando el enlace de descarga ya no existe.
- Formato de archivo inesperado: Cuando se recibe un tipo de archivo diferente al esperado.
- Archivo corrupto o incompleto: Cuando la descarga se interrumpe o el archivo está dañado.
- Ruta no válida: Cuando el directorio de destino no existe o no es accesible.
- Registrar el error con detalles específicos en logs.


**3. Desde el proceso de Talento Humano han presentado la necesidad de automatizar el proceso que se describe a continuación:**

   Una persona todos los días laborales a las 8 am debe revisar y clasificar las hojas de vida que llegan a un correo. La persona las descarga y luego las guarda en la ruta local de carpetas:  CV -> año -> mes. La persona renombra cada hoja de vida como tipoDocumento\_numeroDocumento\_NombreApellido\_cargo.pdf, por ejemplo, CC\_123456789\_PedroPerez\_desarrolladorjrRPA. Todos los archivos los guarda como PDF. 

   El primer día laboral de cada mes construye un reporte de Excel con las hojas de vida recibidas el mes anterior y lo envía este último archivo por correo electrónico al área de Calidad (calidad@hospital.co). 

- **Escriba las posibles excepciones del proceso.**

Excepciones de Correo:

- Correo sin internet o servidor de correo caído.
- Credenciales de acceso incorrectas.
- Correos con adjuntos corruptos.
- Formatos de archivo no soportados en los adjuntos.

Excepciones de Archivos:

- Hojas de vida en formatos no convertibles a PDF.
- Archivos protegidos con contraseña.
- Documentos corruptos o que no permite acceder.

Excepciones de Datos:

- Información faltante en las hojas de vida (nombre, documento de identidad, cargo y/o vacante que aspira).
- Texto no extraíble (imágenes sin texto, o no legibles por el sistema).
- Hojas de vida en idiomas no soportados.

Excepciones del Sistema:

- Espacio insuficiente en disco
- Rutas de red no disponibles..
- Fallo en la conversión a PDF.
- Error al enviar correo del reporte.


- **Escriba las validaciones que considere necesarias.**

Validaciones de Entrada:

- Verificar que el pdf sea realmente una hoja de vida.
- Validar formato de número de documento (solo números y longitud de este).
- Verificar que el nombre contenga solo caracteres válidos, y si no, estandarizar.
- Validar que el cargo sea uno de los predefinidos desde talento humano.

Validaciones de Estructura:

- Confirmar que el archivo se puede convertir a PDF.
- Verificar que se extrajo información mínima requerida.
- Validar que la ruta de destino existe y es accesible.
- Confirmar que no existe ya un archivo con el mismo nombre o credenciales.

Validaciones de Calidad:

- Verificar que el PDF generado no esté corrupto.
- Validar que el tamaño del archivo sea razonable y no sea un virus.
- Confirmar que el reporte Excel se genere correctamente.
- Verificar entrega exitosa del correo mensual (puede llegar un correo al encargado de esta tarea para verificar que sirvió, ya sea correo con las fallas que hubo, logs, y/o éxito de envió).2


- **Indique que módulos o tareas implementaría en el robot describiendo brevemente que haría cada uno/a.**

1\. Módulo de conexión al correo:

- Conectar al correo con credenciales.
- Manejar errores de autenticación y reconexión automática.

2\. Filtrado inteligente de correos:

- Filtrar por asunto buscando palabras como: "CV", "hoja de vida", "currículum", "postulación", “HV”, “vacante” o listado de vacantes disponibles en el momento definidas por talento humano.
- Filtrar por remitente excluyendo correos internos de la empresa, noticias o probables spams.
- Filtrar también por el contenido del correo buscando frases como: "adjunto mi CV", "me postulo para", etc.
- Verificar que tenga adjuntos en formatos .pdf, .doc, .docx o similar.
- Descartar correos masivos y automáticos del sistema.

3\. Descarga y validación de adjuntos

- Descargar solo archivos relevantes (documentos, no imágenes).
- Verificar tamaño del archivo que no exceda una cantidad grande (no pueden ser más de 200mb).
- Validar que el archivo no esté corrupto antes de procesarlo.
- Confirmar que es realmente una hoja de vida revisando el contenido con palabras claves y/o de anclaje.

4\. Extracción de datos

- Extraer nombre y apellidos del documento usando pandas (biblioteca de Python) y/o OCR en su debido caso.
- Extraer número de documento (cédula, pasaporte) con pandas.
- Extraer cargo al que aplica desde el CV o asunto del correo con palabras que define talento humano.
- Identificar tipo de documento (CC, CE, pasaporte).
- Limpiar y validar los datos extraídos.

5\. Conversión

- Convertir todos los archivos a PDF sin importar el formato original.
- Crear nombre del archivo siguiendo el formato: tipoDocumento\_numeroDocumento\_NombreApellido\_cargo.pdf
- Validar que el nombre no tenga caracteres especiales que causen problemas.
- Verificar que no exista ya un archivo con el mismo nombre.

6\. Organización de archivos

- Crear carpetas automáticamente siguiendo la estructura: CV/año/mes.
- Guardar el archivo en la carpeta correspondiente al mes actual.
- Verificar que el archivo se guardó correctamente y no está corrupto.
- Mantener registro de todos los archivos procesados.

7\. Reporte Mensual (Primer día del mes)

- Identificar si es primer día laboral del mes para activar el reporte
- Recopilar datos del mes anterior de hojas de vida procesadas.
- Crear archivo Excel con listado completo y estadísticas.
- Enviar correo automático a <calidad@hospital.co>
- Confirmar entrega exitosa del reporte.

8\. Control y Logging

- Registrar cada acción realizada con fecha y hora.
- Guardar errores encontrados para revisión posterior.
- Marcar correos como procesados para no reprocesarlos.
- Generar alertas cuando hay problemas críticos.
- Crear respaldo de configuraciones importantes.

9\. Manejo de Excepciones

- Reintentar operaciones fallidas hasta 3 veces.
- Mover archivos problemáticos a carpeta de revisión manual.
- Notificar al administrador cuando hay errores críticos ya sea por correo, teams u alguna notificación.
- Continuar procesando otros correos, aunque uno falle.
- Guardar archivos parciales para no perder trabajo.

**Resumen del flujo:**

Ejecución Diaria (8:00 AM de días laborales):

- Conectar al correo y descargar correos nuevos.
- Filtrar correos relevantes (palabras clave + adjuntos + remitente válido).
- Procesar cada hoja de vida: extraer datos personales, convertir a PDF, renombrar según formato estándar.
- Guardar archivos en carpetas CV/año/mes.
- Registrar operaciones y marcar correos como procesados.
- Enviar notificación de éxito y o fallo con logs.

Ejecución Mensual (Primer día laboral del mes):

- Generar reporte Excel con hojas de vida del mes anterior
- Enviar reporte automáticamente a <calidad@hospital.co> y al encargado de este flujo con el éxito y/o error.



- **Si tiene consideraciones adicionales que se deban tener en cuenta en la solución automatizada, por favor escríbalas.** 

- Encriptar credenciales de acceso al correo en archivo config seguro.
- Configurar accesos restringidos a las carpetas de hojas de vida.
- Archivo config editable para ajustar palabras clave de filtrado sin modificar código.
- Lista de remitentes configurable dinámicamente.
- Horarios de ejecución flexibles según días festivos y calendario laboral.
- Backup automático de configuraciones y logs críticos.
- Alertas por correo o teams cuando hay errores.
- Notificaciones de éxito del reporte mensual enviado.
- Límites configurables de archivos procesados por ejecución (para evitar que quede en un bucle por algún tipo de error).
- Cola de reintentos para archivos que fallan temporalmente
- Respaldo diario de archivos procesados a ubicación secundaria


- **Realice un diagrama de flujo (o herramienta similar que considere adecuada) que refleje la solución de la automatización.**

 <img width="247" height="951" alt="Aspose Words a71e6456-67f5-4f35-a0cd-2e5a26400a65 001" src="https://github.com/user-attachments/assets/cc314db2-0588-4e12-a95c-f96a7a026038" />




4. Realice una automatización en Python usando Selenium para que ingrese a la página <https://automationexercise.com/login> y registre 5 nuevos usuarios.

   Comparta el código y demás archivos o elementos que considere necesarios.

   Si tiene algún aspecto a considerar de cualquier tipo (ya sea para la ejecución, con respecto al proceso, excepciones, decisiones etc.) por favor indíquelo.

   En el archivo README.MD e encuentra como ejecutar el proceso.
