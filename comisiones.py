from abc import ABC, abstractmethod
class EstrategiaComision(ABC):
    """El molde, de toda comisión,se debe saber cuanto calcular a partir del monto"""
    @abstractmethod
    def calcular(self, monto):
        pass
class ComisionAhorros(EstrategiaComision):
    """Cuentas de ahorros, serán del 1% del monto"""
    def calcular(self, monto):
        return round(monto * 0.01, 2)

class ComisionCorriente(EstrategiaComision):
    """Cuentas corrientes, es de S/.5"""
    def calcular(self, monto):
        return 5.0
