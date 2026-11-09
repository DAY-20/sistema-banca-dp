from cuenta import Cuenta, CuentaAhorros, CuentaCorriente
class Transferencia:
"""Transferencia ya validada"""
    def __init__(self, origen, destino, monto):
        self.origen = origen
        self.destino = destino
        self.monto = monto

    def __str__(self):
        return (f"Transferencia de S/. {self.monto} "
                f"de {self.origen.titular} a {self.destino.titular}")

class TransferenciaBuilder:
"""Arma una Transferencia paso a paso y la valida"""
    def __init__(self):
        self._origen = None
        self._destino = None
        self._monto = None

    def con_origen(self, cuenta):
        self._origen = cuenta
        return self

    def con_destino(self, cuenta):
        self._destino = cuenta
        return self

    def con_monto(self, monto):
        self._monto = monto
        return self

    def construir(self):
 """Valida y entrega la Transferencia, o lanza un error"""
        if self._origen is None or self._destino is None:
            raise ValueError("Faltan la cuenta origen o la cuenta destino")
        if self._origen is self._destino:
            raise ValueError("La cuenta destino debe ser distinta de la origen")
        if self._monto is None or self._monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        if self._origen.saldo < self._monto:
            raise ValueError("Saldo insuficiente")
        return Transferencia(self._origen, self._destino, self._monto)
