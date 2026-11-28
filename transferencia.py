import math

from cuenta import Cuenta, CuentaAhorros, CuentaCorriente
from comisiones import ComisionAhorros, ComisionCorriente


class Transferencia:
    """ final de transferencia ya validada"""

    def __init__(self, origen, destino, monto, comision=0):
        self.origen = origen
        self.destino = destino
        self.monto = monto
        self.comision = comision
        self.total = monto + comision

    def __str__(self):
        return (f"Transferencia de S/. {self.monto:.2f} "
                f"de {self.origen.titular} a {self.destino.titular} "
                f"| comisión S/. {self.comision:.2f} | total S/. {self.total:.2f}")
class TransferenciaBuilder:
    """ armar una Transferencia y validarla"""
    def __init__(self):
        self._origen = None
        self._destino = None
        self._monto = None
        self._estrategia = None

    def con_origen(self, cuenta):
        self._origen = cuenta
        return self

    def con_destino(self, cuenta):
        self._destino = cuenta
        return self

    def con_monto(self, monto):
        self._monto = monto
        return self

    def con_comision(self, estrategia):
        self._estrategia = estrategia
        return self

    def construir(self):
        """ valida y entrega la Transferencia, o lanza un error"""
        if self._origen is None or self._destino is None:
            raise ValueError("Faltan la cuenta origen o la cuenta destino")
        if self._origen is self._destino:
            raise ValueError("La cuenta destino debe ser distinta de la origen")
        if self._monto is None or not math.isfinite(self._monto) or self._monto <= 0:
            raise ValueError("El monto debe ser un número mayor a cero")

        comision = 0
        if self._estrategia is not None:
            comision = self._estrategia.calcular(self._monto)

        if self._origen.saldo < self._monto + comision:
            raise ValueError("Saldo insuficiente")
        return Transferencia(self._origen, self._destino, self._monto, comision)


if __name__ == "__main__":
    bry = CuentaAhorros("Bry", 500)
    dayanna = CuentaCorriente("Dayanna", 1000)

    # (descripción, origen, destino, monto, estrategia)
    casos = [
        ("Corriente, monto válido", dayanna, bry, 300, ComisionCorriente()),
        ("Ahorros, monto válido", bry, dayanna, 300, ComisionAhorros()),
        ("Monto muy alto", dayanna, bry, 5000, ComisionCorriente()),
        ("Alcanza el monto, no la comisión", dayanna, bry, 998, ComisionCorriente()),
        ("Monto negativo", dayanna, bry, -10, ComisionCorriente()),
        ("Misma cuenta", dayanna, dayanna, 100, ComisionCorriente()),
    ]

    for descripcion, origen, destino, monto, estrategia in casos:
        try:
            transferencia = (TransferenciaBuilder()
                             .con_origen(origen)
                             .con_destino(destino)
                             .con_monto(monto)
                             .con_comision(estrategia)
                             .construir())
            print(f"{descripcion}: {transferencia}")
        except ValueError as error:
            print(f"{descripcion}: no se pudo crear ({error})")
