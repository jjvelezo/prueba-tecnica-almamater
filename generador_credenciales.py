import json
import os
import random
import string
from datetime import date, timedelta
from faker import Faker

def cargar_configuracion(archivo_config="config.json"):
    with open(archivo_config, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("configuracion", {})

config = cargar_configuracion()
fake = Faker(config.get("generacion_usuarios", {}).get("locale_faker", "en_US"))

def generar_contrasena(length=None, use_symbols=None):
    config_pass = config.get("contrasenas", {})
    if length is None:
        length = config_pass.get("longitud", 12)
    if use_symbols is None:
        use_symbols = config_pass.get("usar_simbolos", True)
    
    chars = ""
    if config_pass.get("incluir_minusculas", True):
        chars += string.ascii_lowercase
    if config_pass.get("incluir_mayusculas", True):
        chars += string.ascii_uppercase
    if config_pass.get("incluir_numeros", True):
        chars += string.digits
    
    symbols = config_pass.get("caracteres_especiales", "!@#$%^&*()-_=+[]{};:,.<>/?")
    if use_symbols:
        chars += symbols
    
    password = []
    if config_pass.get("incluir_minusculas", True):
        password.append(random.choice(string.ascii_lowercase))
    if config_pass.get("incluir_mayusculas", True):
        password.append(random.choice(string.ascii_uppercase))
    if config_pass.get("incluir_numeros", True):
        password.append(random.choice(string.digits))
    if use_symbols and symbols:
        password.append(random.choice(symbols))
    
    while len(password) < length:
        password.append(random.choice(chars))
    random.shuffle(password)
    return ''.join(password)

def fecha_nacimiento_aleatoria(min_age=None, max_age=None):
    config_fecha = config.get("fecha_nacimiento", {})
    if min_age is None:
        min_age = config_fecha.get("edad_minima", 18)
    if max_age is None:
        max_age = config_fecha.get("edad_maxima", 80)
    
    today = date.today()
    start_birth = today - timedelta(days=365 * max_age)
    end_birth = today - timedelta(days=365 * min_age)
    delta_days = (end_birth - start_birth).days
    random_days = random.randrange(delta_days + 1)
    dob = start_birth + timedelta(days=random_days)
    return dob.isoformat()  # 'YYYY-MM-DD'

def numero_celular_eeuu():
    config_tel = config.get("telefono", {})
    codigo_pais = config_tel.get("codigo_pais", "+1")
    area = random.randint(
        config_tel.get("area_code_min", 200),
        config_tel.get("area_code_max", 999)
    )
    central = random.randint(
        config_tel.get("central_min", 200),
        config_tel.get("central_max", 999)
    )
    line = random.randint(
        config_tel.get("line_min", 0),
        config_tel.get("line_max", 9999)
    )
    return f"{codigo_pais}{area:03d}{central:03d}{line:04d}"

def generar_usuario(index):
    config_gen = config.get("generacion_usuarios", {})
    config_correo = config.get("correo", {})
    
    nombre = fake.first_name()
    apellido = fake.last_name()
    
    # Generar correo según configuración
    dominio = config_correo.get("dominio", "pruebatecnica.com")
    if config_correo.get("convertir_minusculas", True):
        local = f"{nombre}.{apellido}".lower()
    else:
        local = f"{nombre}.{apellido}"
    
    if config_correo.get("remover_espacios", True):
        local = local.replace(" ", "")
    
    correo = f"{local}{index}@{dominio}"
    
    generos = config.get("generos_disponibles", ["Masculino", "Femenino"])
    pais_defecto = config_gen.get("pais_defecto", "Estados Unidos")

    usuario = {
        "Nombre": nombre,
        "apellido": apellido,
        "Correo": correo,
        "genero": random.choice(generos),
        "contraseña": generar_contrasena(),
        "fecha de nacimiento": fecha_nacimiento_aleatoria(),
        "compañia": fake.company(),
        "direccion": fake.street_address(),
        "pais": pais_defecto,
        "estado": fake.state(),
        "ciudad": fake.city(),
        "codigo zip": fake.zipcode(),
        "numero celular": numero_celular_eeuu()
    }
    return usuario

def guardar_config(usuarios, filename=None):
    config_archivos = config.get("archivos", {})
    mensajes = config.get("mensajes", {})
    
    if filename is None:
        filename = config_archivos.get("nombre_salida", "config.json")
    
    encoding = config_archivos.get("codificacion", "utf-8")
    
    # Cargar configuración existente para preservarla
    try:
        with open(filename, "r", encoding=encoding) as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = {}
    
    # Mantener la configuración y solo actualizar credenciales
    existing_data["credenciales"] = usuarios
    
    with open(filename, "w", encoding=encoding) as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    mensaje = mensajes.get("archivo_guardado", "Credenciales guardadas en {archivo}")
    print(mensaje.format(archivo=os.path.abspath(filename)))

if __name__ == "__main__":
    config_gen = config.get("generacion_usuarios", {})
    mensajes = config.get("mensajes", {})
    
    cantidad = config_gen.get("cantidad_usuarios", 5)
    
    mensaje_inicio = mensajes.get("iniciando_proceso", "Iniciando proceso de generación de usuarios")
    print(mensaje_inicio)
    
    usuarios = [generar_usuario(i) for i in range(1, cantidad + 1)]
    guardar_config(usuarios)
    
    mensaje_resumen = mensajes.get("resumen_usuarios", "Resumen generado ({cantidad} usuarios)")
    print(f"\n{mensaje_resumen.format(cantidad=cantidad)}:")
    
    for u in usuarios:
        print(f"  {u['Nombre']} {u['apellido']}  -  {u['Correo']}  -  {u['pais']}")
