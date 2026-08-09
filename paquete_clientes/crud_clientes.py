

def insertar(cliente, conexionBD):
    """Inserta un nuevo registro usando un diccionario con los datos del cliente."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor()
            sql = """INSERT INTO clientes 
                     (nombre_completo, telefono, correo, direccion, ocupacion, ingresos_mensuales) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (
                cliente["nombre"],
                cliente["telefono"],
                cliente["correo"],
                cliente["direccion"],
                cliente["ocupacion"],
                cliente["ingresos"]
            )
            cursor.execute(sql, valores)
            conexionBD.commit()
            return True
        return False
    except Exception as e:
        print(f"\n\t[ERROR SQL - Insertar Cliente]: {e}")
        return False

def consultar(conexionBD):
    """Devuelve todos los clientes como una LISTA DE DICCIONARIOS."""
    try:
        if conexionBD is not None:
           
            cursor = conexionBD.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes")
            return cursor.fetchall()
        return []
    except Exception as e:
        print(f"\n\t[ERROR SQL - Consultar Clientes]: {e}")
        return []

def buscar(termino, conexionBD):
    """Busca clientes por ID exacto o por coincidencia en el nombre."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor(dictionary=True)
            sql = "SELECT * FROM clientes WHERE id_cliente = %s OR nombre_completo LIKE %s"
            id_busqueda = int(termino) if str(termino).isdigit() else 0
            cursor.execute(sql, (id_busqueda, f"%{termino}%"))
            return cursor.fetchall()
        return []
    except Exception as e:
        print(f"\n\t[ERROR SQL - Buscar Cliente]: {e}")
        return []

def actualizar(id_cliente, cliente_nuevo, conexionBD):
    """Modifica los datos de un cliente existente buscando por su ID."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor()
            sql = """UPDATE clientes SET 
                     nombre_completo = %s, 
                     telefono = %s, 
                     correo = %s, 
                     direccion = %s, 
                     ocupacion = %s, 
                     ingresos_mensuales = %s 
                     WHERE id_cliente = %s"""
            valores = (
                cliente_nuevo["nombre"],
                cliente_nuevo["telefono"],
                cliente_nuevo["correo"],
                cliente_nuevo["direccion"],
                cliente_nuevo["ocupacion"],
                cliente_nuevo["ingresos"],
                id_cliente
            )
            cursor.execute(sql, valores)
            conexionBD.commit()
            return cursor.rowcount > 0
        return False
    except Exception as e:
        print(f"\n\t[ERROR SQL - Actualizar Cliente]: {e}")
        return False

def eliminar(id_cliente, conexionBD):
    """Elimina un cliente por su ID (Por cascada, borrará sus préstamos)."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
            conexionBD.commit()
            return cursor.rowcount > 0
        return False
    except Exception as e:
        print(f"\n\t[ERROR SQL - Eliminar Cliente]: {e}")
        return False

def vaciar(conexionBD):
    """Vacía toda la tabla de clientes reiniciando el contador de IDs."""
    try:
        if conexionBD is not None:
            cursor = conexionBD.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("TRUNCATE TABLE clientes;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conexionBD.commit()
            return True
        return False
    except Exception as e:
        print(f"\n\t[ERROR SQL - Vaciar Tabla Clientes]: {e}")
        return False