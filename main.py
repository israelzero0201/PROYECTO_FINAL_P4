
# Modlo Principal: main.py


import funciones

from paquete_clientes import interfaz_clientes as cli
from paquete_prestamos import interfaz_prestamos as pres

def menuPrincipal():
    print("\n" + "="*55)
    print(f"\t:::: {funciones.NOMBRE_SISTEMA} ::::")
    print("="*55)
    print(" 1.- Módulo de Gestión de Clientes (Solicitantes)")
    print(" 2.- Módulo de Gestión de Préstamos y Créditos")
    print(" 3.- Salir del Sistema")
    print("="*55)
    opcion = input(" Elige un Módulo para trabajar (1-3): ").strip()
    return opcion

def gestionarSubmenuClientes(conexionBD):
  
    opc_cli = "0"
    while opc_cli != "8":
        funciones.borrarPantalla()
        print(f"\n [Estado DB: Conectado a {conexionBD.database}]")
        opc_cli = cli.menuClientes()
        
        match opc_cli:
            case "1":
                funciones.borrarPantalla()
                cli.agregarClientes(conexionBD)
            case "2":
                funciones.borrarPantalla()
                cli.mostrarClientes(conexionBD)
            case "3":
                funciones.borrarPantalla()
                cli.buscarClientes(conexionBD)
            case "4":
                funciones.borrarPantalla()
                cli.modificarClientes(conexionBD)
            case "5":
                funciones.borrarPantalla()
                cli.borrarClientes(conexionBD)
            case "6":
                funciones.borrarPantalla()
                cli.limpiarClientes(conexionBD)
            case "7":
                funciones.borrarPantalla()
                cli.exportarClientesTXT(conexionBD)
            case "8":
                print("\n\t... Regresando al Menú Principal ...")
                funciones.esperarTecla()
            case _:
                funciones.opcionInvalida()

                

def gestionarSubmenuPrestamos(conexionBD):
    opc_pres = "0"
    while opc_pres != "8":
        funciones.borrarPantalla()
        print(f"\n [Estado DB: Conectado a {conexionBD.database}]")
        opc_pres = pres.menuPrestamos()
        
        match opc_pres:
            case "1":
                funciones.borrarPantalla()
                pres.agregarPrestamos(conexionBD)
            case "2":
                funciones.borrarPantalla()
                pres.mostrarPrestamos(conexionBD)
            case "3":
                funciones.borrarPantalla()
                pres.abonarPrestamo(conexionBD)
            case "4":
                funciones.borrarPantalla()
                pres.buscarPrestamos(conexionBD)
            case "5":
                funciones.borrarPantalla()
                pres.borrarPrestamos(conexionBD)
            case "6":
                funciones.borrarPantalla()
                pres.limpiarPrestamos(conexionBD)
            case "7":
                funciones.borrarPantalla()
                pres.exportarPrestamosTXT(conexionBD)
            case "8":
                print("\n\t... Regresando al Menú Principal ...")
                funciones.esperarTecla()
            case _:
                funciones.opcionInvalida()


if __name__ == "__main__":
    funciones.borrarPantalla()
    print(" Inicializando sistema y verificando conexión a MySQL...")

    
    conexionBD = funciones.conectar()
    intentos_conexion = 1 if conexionBD is not None else 0
    
    if conexionBD is not None:
        print(f"\n\t [SUCCESS]: Conexión establecida con éxito en intento #{intentos_conexion}.")
        print(f"\t Base de datos activa: {conexionBD.database}")
        funciones.esperarTecla()
        
        opc = "0"
        while opc != "3":
            funciones.borrarPantalla()
            opc = menuPrincipal()
            
            match opc:
                case "1":
                    gestionarSubmenuClientes(conexionBD)
                case "2":
                    gestionarSubmenuPrestamos(conexionBD)
                case "3":
                    funciones.borrarPantalla()
                    
                    conexionBD.close()
                    funciones.terminar()
                case _:
                    funciones.opcionInvalida()
    else:
        print("\n [ERROR CRÍTICO]: No se pudo iniciar la aplicación por fallo de conexión.")
        print(" Verifica que XAMPP (Apache y MySQL) estén encendidos y vuelve a intentarlo.") 