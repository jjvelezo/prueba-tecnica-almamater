import json
import time
import os
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def cargar_configuracion(archivo_config="config.json"):
    with open(archivo_config, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("configuracion", {}), data.get("credenciales", [])

def configurar_logging():
    """Configura el sistema de logging con archivo con fecha y hora"""
    config_log = config.get("logging", {})
    config_rutas = config.get("rutas", {})
    config_archivos = config.get("archivos", {})
    
    # Crear directorio de logs si no existe
    logs_dir = config_rutas.get("ruta_logs", "./logs").replace("./", "")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Generar nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{timestamp}.log"
    log_filepath = os.path.join(logs_dir, log_filename)
    
    # Configurar logging según parámetros de configuración
    nivel_str = config_log.get("nivel", "INFO")
    nivel = getattr(logging, nivel_str, logging.INFO)
    formato = config_log.get("formato", "%(asctime)s - %(levelname)s - %(message)s")
    encoding = config_archivos.get("codificacion", "utf-8")
    
    # Configurar handlers
    handlers = [
        logging.FileHandler(log_filepath, encoding=encoding),
        logging.StreamHandler()
    ]
    
    logging.basicConfig(
        level=nivel,
        format=formato,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers
    )
    
    return log_filepath

def cargar_credenciales():
    """Carga las credenciales desde config.json y retorna todos los usuarios"""
    mensajes = config.get("mensajes", {})
    archivo_config = "config.json"
    
    try:
        with open(archivo_config, 'r', encoding='utf-8') as file:
            data = json.load(file)
            credenciales = data.get('credenciales', [])
            logging.info(f"Archivo {archivo_config} cargado exitosamente - {len(credenciales)} usuarios encontrados")
            return credenciales
    except FileNotFoundError:
        mensaje_error = mensajes.get("error_conexion", "Error de conexión")
        logging.error(f"{mensaje_error}: No se encontró el archivo {archivo_config}")
        return None
    except (KeyError, IndexError):
        logging.error(f"Formato incorrecto en {archivo_config} o no hay usuarios disponibles")
        return None
    except json.JSONDecodeError:
        logging.error(f"El archivo {archivo_config} no tiene formato JSON válido")
        return None

def traducir_pais(pais_espanol):
    """Traduce el nombre del país de español a inglés"""
    traducciones = {
        "Estados Unidos": "United States",
        "México": "Mexico",
        "España": "Spain",
        "Argentina": "Argentina",
        "Colombia": "Colombia",
        "Chile": "Chile",
        "Perú": "Peru",
        "Venezuela": "Venezuela",
        "Brasil": "Brazil",
        "Canadá": "Canada"
    }
    return traducciones.get(pais_espanol, pais_espanol)  # Si no encuentra traducción, devuelve el original

def completar_formulario_registro(driver, usuario):
    """Completa el formulario detallado de registro con todos los campos"""
    current_step = "Inicialización"
    try:
        logging.info("Completando formulario detallado de registro...")
        logging.info(f"URL actual al iniciar formulario: {driver.current_url}")
        
        # Esperar 3 segundos adicionales para que todo cargue
        current_step = "Espera inicial de carga"
        time.sleep(3)
        
        # Seleccionar género
        current_step = "Selección de género"
        genero = usuario['genero']
        logging.info(f"Intentando seleccionar género: {genero}")
        
        if genero == "Masculino":
            xpath_genero = "/html/body/section/div/div/div/div/form/div[1]/div[1]/label/div/span/input"
            gender_radio = driver.find_element(By.XPATH, xpath_genero)
            gender_radio.click()
            logging.info("Género 'Masculino' seleccionado exitosamente")
        elif genero == "Femenino":
            xpath_genero = "/html/body/section/div/div/div/div/form/div[1]/div[2]/label/div/span/input"
            gender_radio = driver.find_element(By.XPATH, xpath_genero)
            gender_radio.click()
            logging.info("Género 'Femenino' seleccionado exitosamente")
        else:
            logging.warning(f"Género no reconocido: '{genero}'. Valores esperados: 'Masculino' o 'Femenino'")
        
        # Llenar campo de contraseña
        current_step = "Campo de contraseña"
        xpath_password = "/html/body/section/div/div/div/div/form/div[4]/input"
        logging.info(f"Buscando campo de contraseña en: {xpath_password}")
        password_field = driver.find_element(By.XPATH, xpath_password)
        password_field.clear()
        password_field.send_keys(usuario['contraseña'])
        logging.info("Campo 'contraseña' completado exitosamente")
        
        # Scroll después de la contraseña para evitar que se quede "pegado"
        current_step = "Scroll después de contraseña"
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", password_field)
        time.sleep(1)  # Pequeña pausa para el scroll
        
        # Manejar fecha de nacimiento
        current_step = "Procesamiento de fecha de nacimiento"
        fecha_nacimiento = usuario['fecha de nacimiento']
        logging.info(f"Procesando fecha de nacimiento: {fecha_nacimiento}")
        año, mes, dia = fecha_nacimiento.split('-')
        dia_sin_cero = str(int(dia))
        logging.info(f"Fecha parseada - Año: {año}, Mes: {mes}, Día original: {dia}, Día sin ceros: {dia_sin_cero}")
        
        # Seleccionar día
        current_step = "Selección de día"
        xpath_day = "/html/body/section/div/div/div/div/form/div[5]/div/div[1]/div/select"
        logging.info(f"Buscando dropdown de día en: {xpath_day}")
        day_dropdown = driver.find_element(By.XPATH, xpath_day)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", day_dropdown)
        day_select = Select(day_dropdown)
        
        # Mostrar opciones disponibles para debug
        available_days = [option.get_attribute('value') for option in day_select.options if option.get_attribute('value')]
        logging.info(f"Opciones de día disponibles: {available_days[:10]}...")  # Solo primeros 10 para no saturar log
        
        day_select.select_by_value(dia_sin_cero)
        logging.info(f"Día seleccionado exitosamente: {dia_sin_cero}")
        
        # Seleccionar mes
        current_step = "Selección de mes"
        meses = {
            "01": "January", "02": "February", "03": "March", "04": "April",
            "05": "May", "06": "June", "07": "July", "08": "August",
            "09": "September", "10": "October", "11": "November", "12": "December"
        }
        mes_nombre = meses[mes]
        xpath_month = "/html/body/section/div/div/div/div/form/div[5]/div/div[2]/div/select"
        logging.info(f"Buscando dropdown de mes en: {xpath_month}")
        logging.info(f"Intentando seleccionar mes: '{mes_nombre}' (número original: {mes})")
        
        month_dropdown = driver.find_element(By.XPATH, xpath_month)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", month_dropdown)
        month_select = Select(month_dropdown)
        
        # Mostrar opciones disponibles para debug
        available_months = [option.text for option in month_select.options if option.text.strip()]
        logging.info(f"Opciones de mes disponibles: {available_months}")
        
        month_select.select_by_visible_text(mes_nombre)
        logging.info(f"Mes seleccionado exitosamente: {mes_nombre}")
        
        # Seleccionar año
        current_step = "Selección de año"
        xpath_year = "/html/body/section/div/div/div/div/form/div[5]/div/div[3]/div/select"
        logging.info(f"Buscando dropdown de año en: {xpath_year}")
        logging.info(f"Intentando seleccionar año: {año}")
        
        year_dropdown = driver.find_element(By.XPATH, xpath_year)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", year_dropdown)
        year_select = Select(year_dropdown)
        
        # Mostrar rango de años disponibles para debug
        available_years = [option.get_attribute('value') for option in year_select.options if option.get_attribute('value')]
        if available_years:
            logging.info(f"Años disponibles: {available_years[0]} a {available_years[-1]} (total: {len(available_years)})")
        
        year_select.select_by_value(año)
        logging.info(f"Año seleccionado exitosamente: {año}")
        
        # Campos de información personal
        campos_info = [
            ("Nombre", "p[1]/input", usuario['Nombre']),
            ("Apellido", "p[2]/input", usuario['apellido']),
            ("Compañía", "p[3]/input", usuario['compañia']),
            ("Dirección", "p[4]/input", usuario['direccion'])
        ]
        
        for nombre_campo, xpath_relativo, valor in campos_info:
            current_step = f"Campo {nombre_campo}"
            xpath_completo = f"/html/body/section/div/div/div/div/form/{xpath_relativo}"
            logging.info(f"Completando campo '{nombre_campo}' en: {xpath_completo}")
            logging.info(f"Valor a ingresar: '{valor}'")
            
            field = driver.find_element(By.XPATH, xpath_completo)
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", field)
            field.clear()
            field.send_keys(valor)
            logging.info(f"Campo '{nombre_campo}' completado exitosamente")
        
        # País
        current_step = "Selección de país"
        pais_original = usuario['pais']
        pais_traducido = traducir_pais(pais_original)
        xpath_country = "/html/body/section/div/div/div/div/form/p[6]/select"
        logging.info(f"Buscando dropdown de país en: {xpath_country}")
        logging.info(f"País original: '{pais_original}', País traducido: '{pais_traducido}'")
        
        country_dropdown = driver.find_element(By.XPATH, xpath_country)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", country_dropdown)
        country_select = Select(country_dropdown)
        
        # Mostrar países disponibles para debug
        available_countries = [option.text for option in country_select.options if option.text.strip()]
        logging.info(f"Países disponibles: {available_countries[:5]}...")  # Solo primeros 5
        
        country_select.select_by_visible_text(pais_traducido)
        logging.info(f"País seleccionado exitosamente: {pais_traducido}")
        
        # Campos de dirección restantes
        campos_direccion = [
            ("Estado", "p[7]/input", usuario['estado']),
            ("Ciudad", "p[8]/input", usuario['ciudad']),
            ("Código ZIP", "p[9]/input", usuario['codigo zip']),
            ("Número celular", "p[10]/input", usuario['numero celular'])
        ]
        
        for nombre_campo, xpath_relativo, valor in campos_direccion:
            current_step = f"Campo {nombre_campo}"
            xpath_completo = f"/html/body/section/div/div/div/div/form/{xpath_relativo}"
            logging.info(f"Completando campo '{nombre_campo}' en: {xpath_completo}")
            logging.info(f"Valor a ingresar: '{valor}'")
            
            field = driver.find_element(By.XPATH, xpath_completo)
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", field)
            field.clear()
            field.send_keys(valor)
            logging.info(f"Campo '{nombre_campo}' completado exitosamente")
        
        # Hacer clic en el botón final del formulario
        current_step = "Envío del formulario"
        xpath_submit = "/html/body/section/div/div/div/div/form/button"
        logging.info(f"Buscando botón de envío en: {xpath_submit}")
        
        submit_button = driver.find_element(By.XPATH, xpath_submit)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_button)
        time.sleep(1)
        submit_button.click()
        logging.info("Botón de envío presionado exitosamente")
        
        # Esperar 5 segundos antes de continuar
        current_step = "Espera después del envío"
        logging.info("Esperando 5 segundos después del envío...")
        time.sleep(5)
        
        # Verificar URL actual después de completar el formulario
        current_step = "Verificación final"
        current_url = driver.current_url
        logging.info(f"URL actual después de completar formulario: {current_url}")
        
        logging.info("Formulario detallado completado exitosamente")
        return True
        
    except NoSuchElementException as e:
        logging.error(f"ERROR en paso '{current_step}': Elemento no encontrado")
        logging.error(f"Detalles del error: {str(e)}")
        logging.error(f"URL actual: {driver.current_url}")
        time.sleep(3)
        raise e
    except TimeoutException as e:
        logging.error(f"ERROR en paso '{current_step}': Tiempo de espera agotado")
        logging.error(f"Detalles del error: {str(e)}")
        logging.error(f"URL actual: {driver.current_url}")
        time.sleep(3)
        raise e
    except Exception as e:
        logging.error(f"ERROR GENERAL en paso '{current_step}': {type(e).__name__}")
        logging.error(f"Detalles del error: {str(e)}")
        logging.error(f"URL actual: {driver.current_url}")
        logging.error(f"Datos del usuario que causó el error:")
        logging.error(f"  - Nombre: {usuario.get('Nombre', 'N/A')}")
        logging.error(f"  - Email: {usuario.get('Correo', 'N/A')}")
        logging.error(f"  - Género: {usuario.get('genero', 'N/A')}")
        logging.error(f"  - Fecha nacimiento: {usuario.get('fecha de nacimiento', 'N/A')}")
        time.sleep(3)
        raise e

def registrar_usuario_individual(driver, usuario, numero_usuario, intento=1):
    """Registra un usuario individual con lógica de reintentos"""
    config_timeouts = config.get("timeouts", {})
    config_urls = config.get("urls", {})
    
    max_intentos = config_timeouts.get("reintentos_maximos", 2)
    current_step = "Inicialización"
    
    try:
        logging.info(f"=== USUARIO {numero_usuario} - INTENTO {intento}/{max_intentos} ===")
        logging.info(f"Registrando: {usuario['Nombre']} {usuario['apellido']}")
        logging.info(f"Email: {usuario['Correo']}")
        logging.info(f"Género: {usuario['genero']}")
        logging.info(f"Fecha nacimiento: {usuario['fecha de nacimiento']}")
        
        # Navegar a la página de signup usando configuración
        current_step = "Navegación a página de signup"
        url_base = config_urls.get("url_base", "https://automationexercise.com")
        url_registro = config_urls.get("url_registro", "/signup")
        url_completa = f"{url_base.rstrip('/')}{url_registro}"
        
        logging.info(f"Navegando a {url_completa}")
        driver.get(url_completa)
        logging.info(f"URL cargada: {driver.current_url}")
        
        # Esperar a que la página cargue usando configuración
        current_step = "Espera de carga de página"
        tiempo_espera = config_timeouts.get("lectura_timeout", 10)
        wait = WebDriverWait(driver, tiempo_espera)
        logging.info("Esperando que los elementos de la página estén disponibles...")
        
        # Localizar y llenar el campo de nombre en la sección de signup
        current_step = "Campos iniciales de signup"
        logging.info("Completando campos iniciales de registro...")
        
        # Buscar el formulario de "New User Signup!"
        current_step = "Campo de nombre inicial"
        name_selector = "input[name='name']"
        logging.info(f"Buscando campo de nombre con selector: {name_selector}")
        
        name_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, name_selector)))
        logging.info("Campo de nombre encontrado exitosamente")
        name_field.clear()
        name_field.send_keys(usuario['Nombre'])
        logging.info(f"Campo 'name' completado: {usuario['Nombre']}")
        
        # Buscar y llenar el campo de email usando data-qa
        current_step = "Campo de email inicial"
        email_selector = "input[data-qa='signup-email']"
        logging.info(f"Buscando campo de email con selector: {email_selector}")
        
        email_field = driver.find_element(By.CSS_SELECTOR, email_selector)
        logging.info("Campo de email encontrado exitosamente")
        email_field.clear()
        email_field.send_keys(usuario['Correo'])
        logging.info(f"Campo 'email' completado: {usuario['Correo']}")
        
        # Hacer clic en el botón de Signup usando XPath específico
        current_step = "Botón de signup inicial"
        signup_xpath = "/html/body/section/div/div/div[3]/div/form/button"
        logging.info(f"Buscando botón de signup en: {signup_xpath}")
        
        signup_button = driver.find_element(By.XPATH, signup_xpath)
        logging.info("Botón de signup encontrado exitosamente")
        signup_button.click()
        logging.info("Botón 'Signup' presionado")
        
        # Esperar a que se cargue la página del formulario completo
        current_step = "Espera después del signup inicial"
        logging.info("Esperando carga del formulario detallado...")
        time.sleep(3)
        logging.info(f"URL después del signup inicial: {driver.current_url}")
        
        # Completar el formulario de registro detallado
        current_step = "Formulario detallado"
        logging.info("Iniciando completar formulario de registro detallado")
        resultado = completar_formulario_registro(driver, usuario)
        
        if resultado:
            logging.info(f"✓ Usuario {numero_usuario} ({usuario['Nombre']} {usuario['apellido']}) registrado exitosamente en intento {intento}")
            return True
        else:
            raise Exception("Error al completar el formulario de registro detallado")
            
    except NoSuchElementException as e:
        logging.error(f"ELEMENTO NO ENCONTRADO en paso '{current_step}' - Usuario {numero_usuario} - Intento {intento}")
        logging.error(f"Selector/XPath que falló: {str(e)}")
        logging.error(f"URL actual: {driver.current_url}")
        logging.error(f"Título de página: {driver.title}")
        
        # Si hay un error y no hemos alcanzado el máximo de intentos, reintentar
        if intento < max_intentos:
            logging.info(f"Preparando reintento para usuario {numero_usuario}...")
            logging.info(f"Esperando 3 segundos antes del reintento...")
            time.sleep(3)
            
            logging.info(f"Recargando página para reintento...")
            driver.refresh()
            time.sleep(2)
            
            return registrar_usuario_individual(driver, usuario, numero_usuario, intento + 1)
        else:
            logging.error(f"✗ Usuario {numero_usuario} FALLÓ DEFINITIVAMENTE después de {max_intentos} intentos (NoSuchElement)")
            return False
            
    except TimeoutException as e:
        logging.error(f"TIMEOUT en paso '{current_step}' - Usuario {numero_usuario} - Intento {intento}")
        logging.error(f"Elemento que causó timeout: {str(e)}")
        logging.error(f"URL actual: {driver.current_url}")
        logging.error(f"Tiempo de espera excedido esperando elemento")
        
        if intento < max_intentos:
            logging.info(f"Preparando reintento para usuario {numero_usuario}...")
            logging.info(f"Esperando 3 segundos antes del reintento...")
            time.sleep(3)
            
            logging.info(f"Recargando página para reintento...")
            driver.refresh()
            time.sleep(2)
            
            return registrar_usuario_individual(driver, usuario, numero_usuario, intento + 1)
        else:
            logging.error(f"✗ Usuario {numero_usuario} FALLÓ DEFINITIVAMENTE después de {max_intentos} intentos (Timeout)")
            return False
            
    except Exception as e:
        logging.error(f"ERROR GENERAL en paso '{current_step}' - Usuario {numero_usuario} - Intento {intento}")
        logging.error(f"Tipo de error: {type(e).__name__}")
        logging.error(f"Mensaje de error: {str(e)}")
        logging.error(f"URL actual: {driver.current_url}")
        logging.error(f"Datos del usuario:")
        logging.error(f"  - ID: Usuario {numero_usuario}")
        logging.error(f"  - Nombre completo: {usuario['Nombre']} {usuario['apellido']}")
        logging.error(f"  - Email: {usuario['Correo']}")
        logging.error(f"  - Género: {usuario['genero']}")
        
        if intento < max_intentos:
            logging.info(f"Preparando reintento para usuario {numero_usuario}...")
            logging.info(f"Esperando 3 segundos antes del reintento...")
            time.sleep(3)
            
            logging.info(f"Recargando página para reintento...")
            driver.refresh()
            time.sleep(2)
            
            return registrar_usuario_individual(driver, usuario, numero_usuario, intento + 1)
        else:
            logging.error(f"✗ Usuario {numero_usuario} FALLÓ DEFINITIVAMENTE después de {max_intentos} intentos (Error general)")
            return False

def registrar_usuarios():
    """Automatiza el registro de todos los usuarios en automationexercise.com"""
    config_navegador = config.get("navegador", {})
    config_timeouts = config.get("timeouts", {})
    mensajes = config.get("mensajes", {})
    
    # Cargar todas las credenciales
    usuarios = cargar_credenciales()
    if not usuarios:
        return False
    
    # Configurar el navegador
    driver = None
    usuarios_exitosos = 0
    usuarios_fallidos = 0
    
    try:
        # Configurar opciones del navegador
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        
        if config_navegador.get("modo_headless", False):
            chrome_options.add_argument("--headless")
        
        user_agent = config_navegador.get("user_agent", "")
        if user_agent:
            chrome_options.add_argument(f"--user-agent={user_agent}")
        
        # Inicializar Chrome WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        if config_navegador.get("ventana_maximizada", True):
            driver.maximize_window()
        
        # Configurar timeouts
        driver.implicitly_wait(config_timeouts.get("delay_entre_operaciones", 1))
        
        # Procesar cada usuario
        for i, usuario in enumerate(usuarios, 1):
            logging.info(f"\n{'='*50}")
            logging.info(f"PROCESANDO USUARIO {i} DE {len(usuarios)}")
            logging.info(f"{'='*50}")
            
            resultado = registrar_usuario_individual(driver, usuario, i)
            
            if resultado:
                usuarios_exitosos += 1
            else:
                usuarios_fallidos += 1
            
            # Pausa entre usuarios (excepto el último)
            delay = config_timeouts.get("delay_entre_operaciones", 2)
            if i < len(usuarios):
                logging.info(f"Pausa de {delay} segundos antes del siguiente usuario...")
                time.sleep(delay)
        
        # Resumen final
        logging.info(f"\n{'='*50}")
        logging.info("RESUMEN FINAL")
        logging.info(f"{'='*50}")
        logging.info(f"Total usuarios procesados: {len(usuarios)}")
        logging.info(f"Usuarios registrados exitosamente: {usuarios_exitosos}")
        logging.info(f"Usuarios con errores: {usuarios_fallidos}")
        
        return usuarios_fallidos == 0  # True si todos fueron exitosos
        
    except Exception as e:
        logging.error(f"Error general durante el registro de usuarios: {e}")
        return False
    
    finally:
        if driver:
            logging.info("Cerrando navegador...")
            time.sleep(2)  # Pausa para ver el resultado
            driver.quit()

def main():
    """Función principal"""
    config_urls = config.get("urls", {})
    mensajes = config.get("mensajes", {})
    
    # Configurar sistema de logging
    log_filepath = configurar_logging()
    
    url_base = config_urls.get("url_base", "https://automationexercise.com")
    url_registro = config_urls.get("url_registro", "/signup")
    sitio_web = f"{url_base.rstrip('/')}{url_registro}"
    
    logging.info("=== Automatización de Registro de Usuarios ===")
    logging.info(f"Sitio web: {sitio_web}")
    logging.info(f"Log guardado en: {log_filepath}")
    
    mensaje_inicio = mensajes.get("iniciando_proceso", "Iniciando proceso de registro de usuarios")
    logging.info(mensaje_inicio)
    
    resultado = registrar_usuarios()
    
    mensaje_completado = mensajes.get("proceso_completado", "Proceso completado exitosamente")
    mensaje_error = mensajes.get("error_conexion", "Error de conexión")
    
    if resultado:
        logging.info(f"✓ {mensaje_completado}")
    else:
        logging.error(f"✗ {mensaje_error} durante el proceso de registro de usuarios")

if __name__ == "__main__":
    # Cargar configuración global antes de ejecutar
    config, credenciales = cargar_configuracion()
    main()