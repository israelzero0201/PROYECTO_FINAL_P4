

def insertar(prestamo, conexionBD):
    """Inserta un nuevo préstamo vinculando el ID de un cliente existente e iniciando pagos en 0."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor()
            sql = """INSERT INTO prestamos 
                     (id_cliente, monto_inicial, tasa_interes, plazo_meses, pago_mensual, saldo_pendiente, pagos_realizados) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (
                prestamo["id_cliente"],
                prestamo["monto"],
                prestamo["tasa"],
                prestamo["plazo"],
                prestamo["pago_mensual"],
                prestamo["saldo"],
                prestamo["pagos_realizados"]
            )
            cursor.execute(sql, valores)
            conexionBD.commit()
            return True
        return False
    except Exception as e:
        print(f"\n\t[ERROR SQL - Registrar Préstamo]: {e}")
        return False

def consultar(conexionBD):
    """Devuelve todos los préstamos uniendo los nombres de la tabla clientes (INNER JOIN)."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor(dictionary=True)
            sql = """SELECT p.id_prestamo, p.id_cliente, c.nombre_completo, 
                            p.monto_inicial, p.tasa_interes, p.plazo_meses, 
                            p.pago_mensual, p.saldo_pendiente, p.pagos_realizados 
                     FROM prestamos p 
                     INNER JOIN clientes c ON p.id_cliente = c.id_cliente"""
            cursor.execute(sql)
            return cursor.fetchall()
        return []
    except Exception as e:
        print(f"\n\t[ERROR SQL - Consultar Préstamos]: {e}")
        return []

def buscar(termino, conexionBD):
    """Busca préstamos por el ID del préstamo, ID del cliente o Nombre del solicitante."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor(dictionary=True)
            sql = """SELECT p.id_prestamo, p.id_cliente, c.nombre_completo, c.telefono,
                            p.monto_inicial, p.tasa_interes, p.plazo_meses, 
                            p.pago_mensual, p.saldo_pendiente, p.pagos_realizados 
                     FROM prestamos p 
                     INNER JOIN clientes c ON p.id_cliente = c.id_cliente 
                     WHERE p.id_prestamo = %s OR p.id_cliente = %s OR c.nombre_completo LIKE %s"""
            
            id_busqueda = int(termino) if str(termino).isdigit() else 0
            cursor.execute(sql, (id_busqueda, id_busqueda, f"%{termino}%"))
            return cursor.fetchall()
        return []
    except Exception as e:
        print(f"\n\t[ERROR SQL - Buscar Préstamos]: {e}")
        return []

def actualizar(id_prestamo, nuevo_saldo, nuevos_pagos, conexionBD):
    """Actualiza el saldo pendiente y el contador de pagos realizados de un crédito."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor()
            sql = "UPDATE prestamos SET saldo_pendiente = %s, pagos_realizados = %s WHERE id_prestamo = %s"
            cursor.execute(sql, (nuevo_saldo, nuevos_pagos, id_prestamo))
            conexionBD.commit()
            return cursor.rowcount > 0
        return False
    except Exception as e:
        print(f"\n\t[ERROR SQL - Actualizar Saldo y Pagos]: {e}")
        return False

def eliminar(id_prestamo, conexionBD):
    """Elimina un registro de préstamo individual por su ID."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor()
            cursor.execute("DELETE FROM prestamos WHERE id_prestamo = %s", (id_prestamo,))
            conexionBD.commit()
            return cursor.rowcount > 0
        return False
    except Exception as e:
        print(f"\n\t[ERROR SQL - Eliminar Préstamo]: {e}")
        return False

def vaciar(conexionBD):
    """Vacía toda la tabla de préstamos sin afectar el registro de los clientes."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor()
            cursor.execute("TRUNCATE TABLE prestamos;")
            conexionBD.commit()
            return True
        return False
    except Exception as e:
        print(f"\n\t[ERROR SQL - Vaciar Tabla Préstamos]: {e}")
        return False