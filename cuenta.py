class Cuenta:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        self.saldo += monto

    def retirar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        if self.saldo < monto:
            raise ValueError("Saldo insuficiente")
        self.saldo -= monto
