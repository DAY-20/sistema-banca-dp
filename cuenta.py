class Cuenta:
    """Se ha creado la cuenta bancaria base"""
    """Se guarda al titular y su saldo"""
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, monto):
        """Sumar el monto al saldo, el monto debe de ser mayor a cero"""
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        self.saldo += monto

    def retirar(self, monto):
        """Restar el monto del saldo, siempre y cuando alcance"""
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        if self.saldo < monto:
            raise ValueError("Saldo insuficiente")
        self.saldo -= monto
    def mostrar_saldo(self):
        """Imprime el saldo"""
        print(f"{self.titular} tiene S/. {self.saldo}")
#Clases hijas
class CuentaAhorros(Cuenta):
    def tipo(self):
        return "Ahorros"
class CuentaCorriente(Cuenta):
    def tipo(self):
        return "Corriente"
# Prueba 1:
mi_cuenta = CuentaAhorros("DAY", 1000)
mi_cuenta.mostrar_saldo()
# Depósito
try:
    mi_cuenta.depositar(500)
    print("Depósito exitoso")
except ValueError as error:
    print(f"No se pudo depositar: {error}")
mi_cuenta.mostrar_saldo()
# Retiro
try:
    mi_cuenta.retirar(2000)
    print("Retiro exitoso")
except ValueError as error:
    print(f"No se pudo retirar: {error}")
mi_cuenta.mostrar_saldo()











