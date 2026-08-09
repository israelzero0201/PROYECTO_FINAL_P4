

import funciones
from paquete_clientes import crud_clientes

def menuClientes():
    """Muestra el submenú para gestionar clientes y retorna la opción seleccionada."""
    print("\n" + "="*55)
    print("\t::: GESTIÓN DE CLIENTES (SOLICITANTES) :::")
    print("="*55)
    print(" 1.- Registrar Nuevo Cliente")
    print(" 2.- Mostrar Directorio de Clientes (Con Estadísticas)")
    print(" 3.- Buscar Cliente por ID o Nombre")
    print(" 4.- Modificar Datos de un Cliente")
    print(" 5.- Eliminar un Cliente")
    print(" 6.- Vaciar Toda la Tabla de Clientes")
    print(" 7.- Exportar Directorio a Archivo TXT")
    print(" 8.- Regresar al Menú Principal")
    print("="*55)
    opcion = input(" Elige una Opción (1-8): ").strip()
    return opcion

def agregarClientes(conexionBD):
    """Solicita datos por teclado aplicando validaciones RegEx y los envía al CRUD."""
    print("\n\t::::.. REGISTRAR NUEVO CLIENTE ..::::\n")
    op = "SI"
    while op == "SI":
        nombre = funciones.validarTexto(" Escribe el Nombre Completo: ")
        telefono = funciones.validarTelefono(" Escribe el Teléfono (10 dígitos): ")
        correo = funciones.validarCorreo(" Escribe el Correo Electrónico: ")
        
        direccion = ""
        while len(direccion) < 5:
            direccion = input(" Escribe la Dirección Completa: ").strip()
            if len(direccion) < 5:
                print("\t[Error]: La dirección es muy corta.")
                
        ocupacion = funciones.validarTexto(" Escribe la Ocupación o Trabajo: ")
        ingresos = funciones.validarNumeroDecimal(" Escribe los Ingresos Mensuales ($): ")
        
        nuevo_cliente = {
            "nombre": nombre,
            "telefono": telefono,
            "correo": correo,
            "direccion": direccion,
            "ocupacion": ocupacion,
            "ingresos": ingresos
        }
        
        respuesta = crud_clientes.insertar(nuevo_cliente, conexionBD)
        if respuesta:
            funciones.accionExitosa()
        else:
            funciones.accionNoExitosa()
            
        op = input("\n ¿Deseas registrar otro cliente? (SI/NO): ").upper().strip()
        while op not in ["SI", "NO"]:
            op = input(" Por favor, responde SI o NO: ").upper().strip()

def mostrarClientes(conexionBD):
    """Muestra clientes completos sin recortar ningún carácter con contadores y acumuladores."""
    print("\n\t::::.. DIRECTORIO GENERAL DE CLIENTES ..::::\n")
    lista_clientes = crud_clientes.consultar(conexionBD)
    
    if len(lista_clientes) > 0:
        total_ingresos = 0.0  
        contador_clientes = 0 
        ingreso_maximo = 0.0
        
        
        print(f" {'ID':<4} | {'NOMBRE COMPLETO':<28} | {'TELÉFONO':<11} | {'CORREO':<26} | {'DIRECCIÓN':<35} | {'INGRESOS':<12} | {'OCUPACIÓN'}")
        print("-" * 150)
        
        for c in lista_clientes:
            contador_clientes += 1
            ingreso_cliente = float(c['ingresos_mensuales'])
            
            total_ingresos = total_ingresos + ingreso_cliente 
            
            if ingreso_cliente > ingreso_maximo:
                ingreso_maximo = ingreso_cliente
                
           
            print(f" {c['id_cliente']:<4} | {c['nombre_completo']:<28} | {c['telefono']:<11} | {c['correo']:<26} | {c['direccion']:<35} | ${ingreso_cliente:<11,.2f} | {c['ocupacion']}")
            
        promedio_ingresos = total_ingresos / contador_clientes if contador_clientes > 0 else 0.0
        
        print("-" * 150)
        print(f" Total de Clientes Registrados: {contador_clientes}")
        print(f" Ingreso Mensual Promedio del Grupo: ${promedio_ingresos:,.2f}")
        print(f" Ingreso Mensual Más Alto Registrado: ${ingreso_maximo:,.2f}")
    else:
        print("\t... ¡No hay clientes registrados en la base de datos! ...")
        
    funciones.esperarTecla()

def buscarClientes(conexionBD):
    """Permite buscar un cliente y ver toda su ficha técnica."""
    print("\n\t::::.. BUSCAR CLIENTE ..::::\n")
    termino = input(" Escribe el ID o el Nombre del cliente a buscar: ").strip()
    
    resultados = crud_clientes.buscar(termino, conexionBD)
    
    if len(resultados) > 0:
        print(f"\n Se encontró(aron) {len(resultados)} coincidencia(s):\n")
        for c in resultados:
            ingreso_cliente = float(c['ingresos_mensuales'])
            print(" *" * 20)
            print(f" ID Cliente: {c['id_cliente']}")
            print(f" Nombre:     {c['nombre_completo']}")
            print(f" Teléfono:   {c['telefono']}")
            print(f" Correo:     {c['correo']}")
            print(f" Dirección:  {c['direccion']}")
            print(f" Ocupación:  {c['ocupacion']}")
            print(f" Ingresos:   ${ingreso_cliente:,.2f}")
        print(" *" * 20)
    else:
        print("\n\t... No se encontró ningún cliente con ese criterio ...")
        
    funciones.esperarTecla()

def modificarClientes(conexionBD):
    """Actualiza los datos de un cliente verificando primero su existencia."""
    print("\n\t::::.. MODIFICAR DATOS DE CLIENTE ..::::\n")
    id_mod = funciones.validarEntero(" Escribe el ID del cliente que deseas modificar: ")
    
    existente = crud_clientes.buscar(id_mod, conexionBD)
    if len(existente) == 0:
        print("\n\t... ¡El ID de cliente ingresado no existe en el sistema! ...")
        funciones.esperarTecla()
        return

    print(f"\n Modificando a: {existente[0]['nombre_completo']}")
    print(" (Ingresa los nuevos datos a continuación)\n")
    
    nombre = funciones.validarTexto(" Nuevo Nombre Completo: ")
    telefono = funciones.validarTelefono(" Nuevo Teléfono (10 dígitos): ")
    correo = funciones.validarCorreo(" Nuevo Correo: ")
    direccion = input(" Nueva Dirección: ").strip()
    ocupacion = funciones.validarTexto(" Nueva Ocupación: ")
    ingresos = funciones.validarNumeroDecimal(" Nuevos Ingresos Mensuales ($): ")
    
    cliente_modificado = {
        "nombre": nombre,
        "telefono": telefono,
        "correo": correo,
        "direccion": direccion,
        "ocupacion": ocupacion,
        "ingresos": ingresos
    }
    
    if crud_clientes.actualizar(id_mod, cliente_modificado, conexionBD):
        funciones.accionExitosa()
    else:
        funciones.accionNoExitosa()
    funciones.esperarTecla()

def borrarClientes(conexionBD):
    """Elimina un cliente tras una doble confirmación de seguridad."""
    print("\n\t::::.. ELIMINAR CLIENTE ..::::\n")
    id_borrar = int(funciones.validarEntero(" Escribe el ID del cliente a eliminar: "))
    
    existente = crud_clientes.buscar(id_borrar, conexionBD)
    if len(existente) == 0:
        print("\n\t... ¡El ID ingresado no existe! ...")
        funciones.esperarTecla()
        return
        
    print(f"\n ¡ATENCIÓN! Estás a punto de eliminar a: {existente[0]['nombre_completo']}")
    print(" Nota: Si este cliente tiene préstamos registrados, también se borrarán.")
    
    opc = input(" ¿Estás totalmente seguro de proceder? (SI/NO): ").upper().strip()
    if opc == "SI":
        if crud_clientes.eliminar(id_borrar, conexionBD):
            funciones.accionExitosa()
        else:
            funciones.accionNoExitosa()
    else:
        print("\n\t... Operación cancelada por el usuario ...")
    funciones.esperarTecla()

def limpiarClientes(conexionBD):
    """Vacía toda la tabla de clientes con confirmación de seguridad."""
    print("\n\t::::.. VACIAR TABLA DE CLIENTES ..::::\n")
    print(" ¡ADVERTENCIA CRÍTICA! Esto borrará a TODOS los clientes y sus préstamos.")
    opc = input(" ¿Estás seguro de que deseas VACIAR toda la base de datos de clientes? (SI/NO): ").upper().strip()
    
    if opc == "SI":
        if crud_clientes.vaciar(conexionBD):
            funciones.accionExitosa()
        else:
            funciones.accionNoExitosa()
    else:
        print("\n\t... Operación cancelada ...")
    funciones.esperarTecla()

def exportarClientesTXT(conexionBD):
    """Genera un archivo TXT con el reporte general de clientes."""
    print("\n\t::::.. EXPORTANDO DIRECTORIO A ARCHIVO TXT ..::::\n")
    lista_clientes = crud_clientes.consultar(conexionBD)
    
    if len(lista_clientes) == 0:
        print("\t... No hay datos para exportar ...")
        funciones.esperarTecla()
        return
        
    contenido = "REPORTE GENERAL DE CLIENTES REGISTRADOS\n"
    contenido += "==================================================\n\n"
    
    for c in lista_clientes:
        ingreso_cliente = float(c['ingresos_mensuales'])
        contenido += f"ID: {c['id_cliente']} | Nombre: {c['nombre_completo']}\n"
        contenido += f"Tel: {c['telefono']} | Correo: {c['correo']}\n"
        contenido += f"Dirección: {c['direccion']}\n"
        contenido += f"Ocupación: {c['ocupacion']} | Ingresos: ${ingreso_cliente:,.2f}\n"
        contenido += "-" * 50 + "\n"
        
    contenido += f"\nTotal de registros exportados: {len(lista_clientes)}\n"
    
    if funciones.generarArchivoTXT("Directorio_Clientes", contenido):
        print("\n\t¡Revisa la carpeta 'reportes_exportados' en tu proyecto!")
    funciones.esperarTecla()