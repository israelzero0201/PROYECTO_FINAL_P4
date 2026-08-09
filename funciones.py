import mysql.connector
import re
import os


NOMBRE_SISTEMA = "SISTEMA DE GESTIÓN DE PRÉSTAMOS V1.0"
RUTA_ARCHIVOS = "reportes_exportados/"



def borrarPantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def esperarTecla():
    input("\n... ¡Oprima cualquier tecla para continuar! ...")

def terminar():
    print(f"\n.... :::: ¡GRACIAS POR UTILIZAR EL {NOMBRE_SISTEMA}! :::: ....")
    input(".... :::: ¡Vuelva pronto! ::::. ")

def opcionInvalida():
    input("\n\t .... ¡Opción inválida! Oprima cualquier tecla para continuar ...")

def accionExitosa():
    input("\n\t... ¡Acción Realizada con Éxito! ...")

def accionNoExitosa():
    input("\n\t... ¡Esta acción no pudo realizarse en este momento! ...")


def conectar():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            database="bd_prestamos_v1"
        )
        return conexion
    except Exception as e:
        borrarPantalla()
        print(f"\n[ERROR CRÍTICO DE BD]: {e}")
        input("... Por el momento no es posible conectar con la base de datos. Inténtelo más tarde ...")
        return None

def validarTexto(mensaje):
    """Valida que la entrada contenga solo letras y espacios."""
    patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
    while True:
        texto = input(mensaje).strip()
        if re.match(patron, texto) and len(texto) >= 3:
            return texto.upper()
        print("\t[Error]: Ingrese un texto válido sin números ni caracteres especiales (mínimo 3 letras).")

def validarTelefono(mensaje):
    """Valida exactamente 10 dígitos numéricos."""
    patron = r'^\d{10}$'
    while True:
        tel = input(mensaje).strip()
        if re.match(patron, tel):
            return tel
        print("\t[Error]: El teléfono debe contener exactamente 10 dígitos numéricos.")

def validarCorreo(mensaje):
    """Valida formato de correo electrónico estándar."""
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    while True:
        correo = input(mensaje).strip()
        if re.match(patron, correo):
            return correo.lower()
        print("\t[Error]: Formato de correo electrónico incorrecto (ejemplo@dominio.com).")

def validarNumeroDecimal(mensaje):
    """Valida enteros positivos o decimales (ej. ingresos o montos)."""
    patron = r'^\d+(\.\d{1,2})?$'
    while True:
        val = input(mensaje).strip()
        if re.match(patron, val) and float(val) > 0:
            return float(val)
        print("\t[Error]: Ingrese un monto numérico positivo válido (ej. 1500 o 1500.50).")

def validarEntero(mensaje):
    """Valida enteros positivos (ej. plazo en meses o IDs)."""
    patron = r'^\d+$'
    while True:
        val = input(mensaje).strip()
        if re.match(patron, val) and int(val) > 0:
            return int(val)
        print("\t[Error]: Ingrese un número entero positivo válido.")


def generarArchivoTXT(nombre_archivo, contenido_texto):
    """Crea un archivo TXT físico en la computadora con el reporte generado."""
    try:
        
        if not os.path.exists(RUTA_ARCHIVOS):
            os.makedirs(RUTA_ARCHIVOS)
            
        ruta_completa = os.path.join(RUTA_ARCHIVOS, f"{nombre_archivo}.txt")
        
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            archivo.write(f"==================================================\n")
            archivo.write(f"          {NOMBRE_SISTEMA}          \n")
            archivo.write(f"==================================================\n\n")
            archivo.write(contenido_texto)
            archivo.write(f"\n==================================================\n")
            archivo.write(f"Fin del Reporte.\n")
            
        print(f"\n\t[SUCCESS]: Archivo generado exitosamente en: {ruta_completa}")
        return True
    except Exception as e:
        print(f"\n\t[ERROR]: No se pudo generar el archivo: {e}")
        return False