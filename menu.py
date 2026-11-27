from cuenta import CuentaAhorros, CuentaCorriente
def crear_cuentas():
    """cuentasguardadas en un diccionario por nombre"""
    cuentas = [
        CuentaCorriente("Dayanna", 2000),
        CuentaAhorros("Bry", 500),
        CuentaCorriente("Vali", 150000),
    ]
    return {cuenta.titular.lower(): cuenta for cuenta in cuentas}

def buscar_cuenta(cuentas, nombre):
    """busca una cuenta por el nombre del titular, o lanza un error"""
    cuenta = cuentas.get(nombre.strip().lower())
    if cuenta is None:
        raise ValueError(f"No existe la cuenta de '{nombre}'")
    return cuenta

def main():
    cuentas = crear_cuentas()

    print(" BANCO DIGITAL ")
    while True:
        try:
            origen = buscar_cuenta(cuentas, input("Tu nombre de titular: "))
            break
        except ValueError as error:
            print(error)

    while True:
        print(f"\n Cliente: {origen.titular} (cuenta {origen.tipo()})")
        print("1. Consultar saldo")
        print("4. Salir")
        opcion = input("Elige una opción: ").strip()
      
        if opcion == "1":
            origen.mostrar_saldo()
        elif opcion == "4":
            print("Hasta luego")
            break
        else:
            print("Opción no válida")
# Prueba
if __name__ == "__main__":
    main()