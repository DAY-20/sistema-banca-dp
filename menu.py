from cuenta import CuentaAhorros, CuentaCorriente
from comisiones import ComisionAhorros, ComisionCorriente
from transferencia import TransferenciaBuilder
from aprobacion import CajeroAutomatico, Supervisor, ComiteRiesgo
from ejecucion import EjecutorReal, ProxyAutenticacion
from auditoria import RegistroAuditoria
from servicio import ServicioTransferencias

# que cada estrategia de comisión corresponde a cada tipo de cuenta
COMISIONES = {
    "Ahorros": ComisionAhorros(),
    "Corriente": ComisionCorriente(),
}

def crear_cuentas():
    """las cuentas de ejemplo, guardadas en un diccionario por nombree"""
    cuentas = [
        CuentaCorriente("Dayanna", 2000),
        CuentaAhorros("Bry", 500),
        CuentaCorriente("Vali", 150000),
    ]
    return {cuenta.titular.lower(): cuenta for cuenta in cuentas}

def crear_cadena_aprobacion():
    """ el cajero -> supervisor -> comité de riesgo."""
    cajero = CajeroAutomatico()
    cajero.establecer_siguiente(Supervisor()).establecer_siguiente(ComiteRiesgo())
    return cajero

def buscar_cuenta(cuentas, nombre):
    """busca una cuenta por el nombre del titular, o lanza un error"""
    cuenta = cuentas.get(nombre.strip().lower())
    if cuenta is None:
        raise ValueError(f"No existe la cuenta de '{nombre}'")
    return cuenta

def leer_monto(mensaje):
    """ pide un monto y lo convierte a número, o lanza un error"""
    texto = input(mensaje)
    try:
        return float(texto)
    except ValueError:
        raise ValueError("El monto debe ser un número")

def hacer_transferencia(origen, cuentas, servicio):
    """pide los datos, arma la transferencia y la envía al servicio"""
    try:
        destino = buscar_cuenta(cuentas, input("Titular de la cuenta destino: "))
        monto = leer_monto("Monto a transferir: S/. ")
        transferencia = (TransferenciaBuilder()
                         .con_origen(origen)
                         .con_destino(destino)
                         .con_monto(monto)
                         .con_comision(COMISIONES[origen.tipo()])
                         .construir())
        print(f"Resumen: {transferencia}")
        aprobador = servicio.transferir(transferencia)
        print(f"Transferencia exitosa (aprobada por {aprobador})")
    except (ValueError, PermissionError) as error:
        print(f"No se pudo completar: {error}")

def elegir_cliente(cuentas):
    """ se pide el nombre del titular, y devuelve su cuenta, o none(nada) si escribe 'salir'."""
    print("Cuentas de prueba:", ", ".join(c.titular for c in cuentas.values()))
    while True:
        nombre = input("Tu nombre de titular (o 'salir'): ")
        if nombre.strip().lower() == "salir":
            return None
        try:
            return buscar_cuenta(cuentas, nombre)
        except ValueError as error:
            print(error)

def menu_cliente(origen, cuentas, servicio, auditoria):
    """menú del cliente, se dvuelve True si quiere cambiar de usuario, False si sale"""
    while True:
        print(f"\n--- Cliente: {origen.titular} \n--- (Cuenta {origen.tipo()}) ---")
        print("1. Consultar saldo")
        print("2. Hacer transferencia")
        print("3. Ver historial de auditoría")
        print("4. Cambiar de usuario")
        print("5. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            origen.mostrar_saldo()
        elif opcion == "2":
            hacer_transferencia(origen, cuentas, servicio)
        elif opcion == "3":
            auditoria.mostrar()
        elif opcion == "4":
            return True
        elif opcion == "5":
            return False
        else:
            print("Opción no válida")

def main():
    cuentas = crear_cuentas()
    auditoria = RegistroAuditoria()
    servicio = ServicioTransferencias(
        crear_cadena_aprobacion(),
        ProxyAutenticacion(EjecutorReal()),
        auditoria,
    )

    print("==== BANCO DIGITAL ====")
    while True:
        origen = elegir_cliente(cuentas)
        if origen is None:
            break
        if not menu_cliente(origen, cuentas, servicio, auditoria):
            break
    print("¡Hasta luego, gracias :3!")

if __name__ == "__main__":
    main()