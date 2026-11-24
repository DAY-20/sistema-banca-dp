import random
from abc import ABC, abstractmethod

class EjecutorTransferencia(ABC):
    """todo ejecutor sabe ejecutar una transferencia"""
    @abstractmethod
    def ejecutar(self, transferencia):
        pass
      
class EjecutorReal(EjecutorTransferencia):
    """el que mueve el dinero"""
    def ejecutar(self, transferencia):
        transferencia.origen.retirar(transferencia.total)
        transferencia.destino.depositar(transferencia.monto)
      
def _codigo_aleatorio():
    return str(random.randint(100000, 999999))

class ProxyAutenticacion(EjecutorTransferencia):
    """el guardia: pide un código 2FA antes de dejar pasar"""

    def __init__(self, ejecutor_real, pedir_codigo=input,
                 generar_codigo=_codigo_aleatorio):
        self._ejecutor_real = ejecutor_real
        self._pedir_codigo = pedir_codigo
        self._generar_codigo = generar_codigo

    def ejecutar(self, transferencia):
        codigo = self._generar_codigo()
        print(f"[SMS simulado] Tu código de verificación es: {codigo}")
        ingresado = self._pedir_codigo("Ingresa el código: ")
        if ingresado != codigo:
            raise PermissionError("Código 2FA incorrecto")
        self._ejecutor_real.ejecutar(transferencia)

if __name__ == "__main__":
    from cuenta import CuentaAhorros, CuentaCorriente
    from comisiones import ComisionCorriente
    from transferencia import TransferenciaBuilder

    bry = CuentaAhorros("Bry", 500)
    dayanna = CuentaCorriente("Dayanna", 1000)

    transferencia = (TransferenciaBuilder()
                     .con_origen(dayanna)
                     .con_destino(bry)
                     .con_monto(300)
                     .con_comision(ComisionCorriente())
                     .construir())

    ejecutor = ProxyAutenticacion(EjecutorReal())
    try:
        ejecutor.ejecutar(transferencia)
        print("Transferencia ejecutada")
    except PermissionError as error:
        print(f"Transferencia bloqueada: {error}")

    dayanna.mostrar_saldo()
    bry.mostrar_saldo()
