

import funciones
from paquete_prestamos import crud_prestamos
from paquete_clientes import crud_clientes

def menuPrestamos():
    """Muestra el menú de gestión de créditos y retorna la opción elegida."""
    print("\n" + "="*55)
    print("\t::: GESTIÓN DE PRÉSTAMOS Y CRÉDITOS :::")
    print("="*55)
    print(" 1.- Solicitar y Registrar Nuevo Préstamo")
    print(" 2.- Mostrar Carteras de Crédito (Con Totales, Desglose y Pagos)")
    print(" 3.- Registrar Pago / Abono a Préstamo (Incrementar Contador)")
    print(" 4.- Buscar Préstamo por ID o Solicitante")
    print(" 5.- Eliminar un Registro de Préstamo")
    print(" 6.- Vaciar Toda la Tabla de Préstamos")
    print(" 7.- Exportar Reporte de Créditos a Archivo TXT")
    print(" 8.- Regresar al Menú Principal")
    print("="*55)
    opcion = input(" Elige una Opción (1-8): ").strip()
    return opcion

def agregarPrestamos(conexionBD):
    """Registra un préstamo verificando al cliente y ejecutando fórmulas de cálculo."""
    print("\n\t::::.. REGISTRAR NUEVO PRÉSTAMO ..::::\n")
    
    id_cliente = int(funciones.validarEntero(" Escribe el ID del Cliente solicitante: "))
    cliente_encontrado = crud_clientes.buscar(id_cliente, conexionBD)
    
    if len(cliente_encontrado) == 0:
        print("\n\t[Error]: No existe ningún cliente con ese ID. Regístrelo primero en el módulo de Clientes.")
        funciones.esperarTecla()
        return
        
    nombre_solicitante = cliente_encontrado[0]['nombre_completo']
    ingresos_solicitante = float(cliente_encontrado[0]['ingresos_mensuales'])
    print(f"\n Solicitante encontrado: {nombre_solicitante} | Ingresos: ${ingresos_solicitante:,.2f}\n")
    
    op = "SI"
    while op == "SI":
        monto = float(funciones.validarNumeroDecimal(" Monto del Préstamo a solicitar ($): "))
        tasa = float(funciones.validarNumeroDecimal(" Tasa de Interés Anual (Ej. 15 para 15%): "))
        plazo = int(funciones.validarEntero(" Plazo de pago en meses (Ej. 12, 24, 36): "))
        
        tasa_decimal = tasa / 100.0
        interes_total = (monto * tasa_decimal) * (plazo / 12.0)
        deuda_total = monto + interes_total
        pago_mensual = deuda_total / plazo
        
        print("\n" + "-"*55)
        print(" RESUMEN DE SIMULACIÓN FINANCIERA:")
        print(f" -> Monto Solicitado (Capital):  ${monto:,.2f}")
        print(f" -> Interés Neto ({tasa}% anual):    ${interes_total:,.2f}")
        print(f" -> VALOR TOTAL DEL PRÉSTAMO:    ${deuda_total:,.2f}")
        print(f" -> CUOTA MENSUAL:               ${pago_mensual:,.2f} por {plazo} meses")
        print("-" * 55)
        
        limite_capacidad = ingresos_solicitante * 0.50
        if pago_mensual > limite_capacidad:
            print(f"\n [ALERTA DE RIESGO]: La cuota excede el 50% de los ingresos del cliente (${limite_capacidad:,.2f}).")
            confirmar = input(" ¿Deseas aprobar el préstamo de todos modos? (SI/NO): ").upper().strip()
            if confirmar != "SI":
                print("\n\t... Préstamo rechazado por seguridad financiera ...")
                funciones.esperarTecla()
                return
        
        nuevo_prestamo = {
            "id_cliente": id_cliente,
            "monto": monto,
            "tasa": tasa,
            "plazo": plazo,
            "pago_mensual": pago_mensual,
            "saldo": deuda_total,
            "pagos_realizados": 0 
        }
        
        if crud_prestamos.insertar(nuevo_prestamo, conexionBD):
            funciones.accionExitosa()
        else:
            funciones.accionNoExitosa()
            
        op = input("\n ¿Deseas registrar otro préstamo para este cliente? (SI/NO): ").upper().strip()
        while op not in ["SI", "NO"]:
            op = input(" Por favor, responde SI o NO: ").upper().strip()

def mostrarPrestamos(conexionBD):
    """Muestra la tabla de créditos incluyendo la columna PAGOS (ej. 1/12)."""
    print("\n\t::::.. CARTERA GENERAL DE PRÉSTAMOS ..::::\n")
    lista_prestamos = crud_prestamos.consultar(conexionBD)
    
    if len(lista_prestamos) > 0:
        contador_creditos = 0
        acum_monto = 0.0
        acum_interes = 0.0
        acum_total_deuda = 0.0
        acum_saldo = 0.0
        
        
        print(f" {'ID':<3} | {'CLIENTE':<24} | {'CAP. INICIAL':<12} | {'TASA %':<7} | {'INT. NETO':<10} | {'TOTAL DEUDA':<11} | {'CUOTA/MES':<10} | {'PAGOS':<7} | {'SALDO ACTUAL'}")
        print("-" * 130)
        
        for p in lista_prestamos:
            contador_creditos += 1
            
            monto_ini = float(p['monto_inicial'])
            tasa = float(p['tasa_interes'])
            plazo = int(p['plazo_meses'])
            saldo_pend = float(p['saldo_pendiente'])
            cuota_mes = float(p['pago_mensual'])
            pagos_hechos = int(p['pagos_realizados'])
            
            interes_neto = (monto_ini * (tasa / 100.0)) * (plazo / 12.0)
            valor_total_prestamo = monto_ini + interes_neto
            
            acum_monto += monto_ini
            acum_interes += interes_neto
            acum_total_deuda += valor_total_prestamo
            acum_saldo += saldo_pend
            
            estado = "LIQUIDADO" if saldo_pend <= 0.01 else f"${saldo_pend:,.2f}"
            tasa_formateada = f"{tasa}%"
            formato_pagos = f"{pagos_hechos}/{plazo}"
            
            print(f" {p['id_prestamo']:<3} | {p['nombre_completo']:<24} | ${monto_ini:<11,.2f} | {tasa_formateada:<7} | ${interes_neto:<9,.2f} | ${valor_total_prestamo:<10,.2f} | ${cuota_mes:<9,.2f} | {formato_pagos:<7} | {estado}")
            
        print("-" * 130)
        print(f" Total de Créditos Emitidos:       {contador_creditos}")
        print(f" Capital Original Prestado:      ${acum_monto:,.2f}")
        print(f" Intereses Netos Generados:      ${acum_interes:,.2f}")
        print(f" Valor Total Emitido en Deuda:   ${acum_total_deuda:,.2f}")
        print(f" Saldo Total Pendiente de Cobro: ${acum_saldo:,.2f}")
    else:
        print("\t... ¡No hay préstamos registrados en el sistema! ...")
        
    funciones.esperarTecla()

def abonarPrestamo(conexionBD):
    """Abona un pago, calcula el desglose e INCREMENTA EL CONTADOR DE PAGOS EN +1."""
    print("\n\t::::.. REGISTRAR PAGO O ABONO A PRÉSTAMO ..::::\n")
    id_prestamo = int(funciones.validarEntero(" Escribe el ID del Préstamo al que deseas abonar: "))
    
    credito = crud_prestamos.buscar(id_prestamo, conexionBD)
    if len(credito) == 0:
        print("\n\t[Error]: No se encontró ningún crédito con ese ID.")
        funciones.esperarTecla()
        return
        
    actual = credito[0]
    monto_ini = float(actual['monto_inicial'])
    tasa = float(actual['tasa_interes'])
    plazo = int(actual['plazo_meses'])
    saldo_actual = float(actual['saldo_pendiente'])
    cuota_mes = float(actual['pago_mensual'])
    pagos_actuales = int(actual['pagos_realizados'])
    
    if saldo_actual <= 0.01:
        print(f"\n\t¡Este préstamo de {actual['nombre_completo']} YA ESTÁ TOTALMENTE LIQUIDADO! (Saldo: $0.00)")
        funciones.esperarTecla()
        return
        
    interes_neto = (monto_ini * (tasa / 100.0)) * (plazo / 12.0)
    valor_total_deuda = monto_ini + interes_neto
    
    print("\n" + "="*50)
    print(f" ESTADO FINANCIERO DEL CRÉDITO #{id_prestamo} ({actual['nombre_completo']}):")
    print("="*50)
    print(f" -> Monto Solicitado (Capital):  ${monto_ini:,.2f}")
    print(f" -> Interés Neto ({tasa}%):         ${interes_neto:,.2f}")
    print(f" -> VALOR TOTAL DEL PRÉSTAMO:    ${valor_total_deuda:,.2f}")
    print("-" * 50)
    print(f" -> Pagos Realizados hasta hoy:  {pagos_actuales} de {plazo} meses")
    print(f" -> SALDO PENDIENTE ACTUAL:      ${saldo_actual:,.2f}")
    print(f" -> Cuota Mensual Sugerida:      ${cuota_mes:,.2f}")
    print("="*50 + "\n")
    
    abono = float(funciones.validarNumeroDecimal(" Escribe el monto que el cliente va a pagar ($): "))
    
    if abono > saldo_actual:
        print(f" Nota: El abono supera la deuda. Se ajustará el cobro a la liquidación exacta (${saldo_actual:,.2f}).")
        abono = saldo_actual
        
    porcentaje_capital = monto_ini / valor_total_deuda
    porcentaje_interes = interes_neto / valor_total_deuda
    
    abono_capital = abono * porcentaje_capital
    abono_interes = abono * porcentaje_interes
    nuevo_saldo = saldo_actual - abono
    
    
    nuevos_pagos = pagos_actuales + 1
    
    print("\n" + "*"*50)
    print(" DESGLOSE DEL PAGO (AMORTIZACIÓN PROPORCIONAL):")
    print("*"*50)
    print(f" -> Monto Total Abonado:     ${abono:,.2f}")
    print(f" -> Abono a Capital:         ${abono_capital:,.2f} ({(porcentaje_capital*100):.1f}%)")
    print(f" -> Abono a Intereses:       ${abono_interes:,.2f} ({(porcentaje_interes*100):.1f}%)")
    print("-" * 50)
    print(f" -> Nuevo conteo de pagos:   {nuevos_pagos} de {plazo} meses")
    print(f" -> SALDO TOTAL RESTANTE:    ${nuevo_saldo:,.2f} (de los ${valor_total_deuda:,.2f} totales)")
    print("*"*50)
    
    opc = input("\n ¿Confirmar aplicación del pago a la base de datos? (SI/NO): ").upper().strip()
    if opc == "SI":
        if crud_prestamos.actualizar(id_prestamo, nuevo_saldo, nuevos_pagos, conexionBD):
            if nuevo_saldo <= 0.01:
                print("\n\t *** ¡FELICIDADES! EL CLIENTE HA LIQUIDADO SU PRÉSTAMO EN SU TOTALIDAD ***")
            funciones.accionExitosa()
        else:
            funciones.accionNoExitosa()
    else:
        print("\n\t... Operación cancelada ...")
    funciones.esperarTecla()

def buscarPrestamos(conexionBD):
    """Busca un préstamo y muestra su desglose y número de pagos realizados."""
    print("\n\t::::.. BUSCAR PRÉSTAMO ..::::\n")
    termino = input(" Escribe el ID del Préstamo, ID del Cliente o Nombre: ").strip()
    
    resultados = crud_prestamos.buscar(termino, conexionBD)
    if len(resultados) > 0:
        print(f"\n Se encontró(aron) {len(resultados)} crédito(s):\n")
        for p in resultados:
            monto_ini = float(p['monto_inicial'])
            tasa = float(p['tasa_interes'])
            plazo = int(p['plazo_meses'])
            cuota_mes = float(p['pago_mensual'])
            saldo_pend = float(p['saldo_pendiente'])
            pagos_hechos = int(p['pagos_realizados'])
            
            interes_neto = (monto_ini * (tasa / 100.0)) * (plazo / 12.0)
            valor_total_deuda = monto_ini + interes_neto
            capital_pagado = valor_total_deuda - saldo_pend
            
            print(" *" * 25)
            print(f" ID Préstamo:        {p['id_prestamo']} (Cliente ID: {p['id_cliente']})")
            print(f" Titular:            {p['nombre_completo']}")
            print(f" Monto Solicitado:   ${monto_ini:,.2f}")
            print(f" Interés Neto:       ${interes_neto:,.2f} ({tasa}% anual a {plazo} meses)")
            print(f" VALOR TOTAL DEUDA:  ${valor_total_deuda:,.2f}")
            print(f" Cuota Mensual:      ${cuota_mes:,.2f}")
            print("-" * 50)
            print(f" Pagos Realizados:   {pagos_hechos} de {plazo} cuotas mensuales")
            print(f" Total Pagado ($):   ${capital_pagado:,.2f}")
            print(f" SALDO PENDIENTE:    ${saldo_pend:,.2f}")
        print(" *" * 25)
    else:
        print("\n\t... No se encontraron préstamos con ese criterio ...")
    funciones.esperarTecla()

def borrarPrestamos(conexionBD):
    """Elimina un registro individual de préstamo tras confirmar."""
    print("\n\t::::.. ELIMINAR PRÉSTAMO ..::::\n")
    id_borrar = int(funciones.validarEntero(" Escribe el ID del Préstamo a eliminar: "))
    
    existente = crud_prestamos.buscar(id_borrar, conexionBD)
    if len(existente) == 0:
        print("\n\t[Error]: No existe ningún préstamo con ese ID.")
        funciones.esperarTecla()
        return
        
    saldo_pend = float(existente[0]['saldo_pendiente'])
    print(f"\n Estás a punto de borrar el crédito #{id_borrar} de: {existente[0]['nombre_completo']}")
    print(f" Saldo pendiente que se cancelará: ${saldo_pend:,.2f}")
    
    opc = input(" ¿Estás totalmente seguro? (SI/NO): ").upper().strip()
    if opc == "SI":
        if crud_prestamos.eliminar(id_borrar, conexionBD):
            funciones.accionExitosa()
        else:
            funciones.accionNoExitosa()
    else:
        print("\n\t... Operación cancelada ...")
    funciones.esperarTecla()

def limpiarPrestamos(conexionBD):
    """Vacía toda la tabla de préstamos."""
    print("\n\t::::.. VACIAR TABLA DE PRÉSTAMOS ..::::\n")
    print(" ¡ADVERTENCIA! Esto borrará TODOS los créditos registrados en la empresa.")
    opc = input(" ¿Estás seguro de VACIAR la tabla de préstamos? (SI/NO): ").upper().strip()
    
    if opc == "SI":
        if crud_prestamos.vaciar(conexionBD):
            funciones.accionExitosa()
        else:
            funciones.accionNoExitosa()
    else:
        print("\n\t... Operación cancelada ...")
    funciones.esperarTecla()

def exportarPrestamosTXT(conexionBD):
    """Genera un archivo TXT con el reporte y desglose general de la cartera de créditos."""
    print("\n\t::::.. EXPORTANDO CARTERA A ARCHIVO TXT ..::::\n")
    lista = crud_prestamos.consultar(conexionBD)
    
    if len(lista) == 0:
        print("\t... No hay datos de préstamos para exportar ...")
        funciones.esperarTecla()
        return
        
    contenido = "REPORTE Y ESTADO FINANCIERO DE CARTERA DE PRÉSTAMOS\n"
    contenido += "==================================================\n\n"
    
    total_monto = 0.0
    total_interes = 0.0
    total_deuda = 0.0
    total_saldo = 0.0
    
    for p in lista:
        monto_ini = float(p['monto_inicial'])
        tasa = float(p['tasa_interes'])
        plazo = int(p['plazo_meses'])
        cuota_mes = float(p['pago_mensual'])
        saldo_pend = float(p['saldo_pendiente'])
        pagos_hechos = int(p['pagos_realizados'])
        
        interes_neto = (monto_ini * (tasa / 100.0)) * (plazo / 12.0)
        valor_total = monto_ini + interes_neto
        
        total_monto += monto_ini
        total_interes += interes_neto
        total_deuda += valor_total
        total_saldo += saldo_pend
        
        contenido += f"Crédito #{p['id_prestamo']} | Titular: {p['nombre_completo']}\n"
        contenido += f" -> Monto Solicitado (Capital):  ${monto_ini:,.2f}\n"
        contenido += f" -> Interés Neto ({tasa}%):         ${interes_neto:,.2f}\n"
        contenido += f" -> Valor Total Préstamo:        ${valor_total:,.2f}\n"
        contenido += f" -> Cuota Mensual:               ${cuota_mes:,.2f} a {plazo} meses\n"
        contenido += f" -> Progreso de Pagos:           {pagos_hechos} de {plazo} cuotas mensuales\n"
        contenido += f" -> SALDO ACTUAL PENDIENTE:      ${saldo_pend:,.2f}\n"
        contenido += "-" * 50 + "\n"
        
    contenido += f"\nRESUMEN GLOBAL DE LA CARTERA ({len(lista)} créditos):\n"
    contenido += f"Total Capital Prestado:   ${total_monto:,.2f}\n"
    contenido += f"Total Intereses Netos:    ${total_interes:,.2f}\n"
    contenido += f"Valor Total en Deuda:     ${total_deuda:,.2f}\n"
    contenido += f"Saldo Total por Cobrar:   ${total_saldo:,.2f}\n"
    
    if funciones.generarArchivoTXT("Cartera_Prestamos_Desglose", contenido):
        print("\n\t¡Revisa la carpeta 'reportes_exportados' para ver el archivo generado!")
    funciones.esperarTecla()