from abc import ABC, abstractmethod

class Aprobador(ABC):
    """ aqui aprueba o pasa la transferencia al siguiente"""
    nombre = "Aprobador"
    def __init__(self):
        self._siguiente = None

    def establecer_siguiente(self, siguiente):
        """ indica quién sigue en la cadena y lo devuelve, para encadenar"""
        self._siguiente = siguiente
        return siguiente

    @abstractmethod
    def puede_aprobar(self, transferencia):
        pass

    def aprobar(self, transferencia):
        """ devuelve quién aprobó, o lanza un error si nadie puede"""
        if self.puede_aprobar(transferencia):
            return self.nombre
        if self._siguiente is None:
            raise ValueError("El monto supera todos los límites de aprobación")
        return self._siguiente.aprobar(transferencia)

class CajeroAutomatico(Aprobador):
    nombre = "Cajero automático"
    def puede_aprobar(self, transferencia):
        return transferencia.monto <= 1000

class Supervisor(Aprobador):
    nombre = "Supervisor"
    def puede_aprobar(self, transferencia):
        return transferencia.monto <= 10000

class ComiteRiesgo(Aprobador):
    nombre = "Comité de riesgo"
    def puede_aprobar(self, transferencia):
        return transferencia.monto <= 100000

if __name__ == "__main__":
    from cuenta import CuentaCorriente
    from transferencia import Transferencia

    origen = CuentaCorriente("Dayanna", 1000000)
    destino = CuentaCorriente("Bry", 0)

    cajero = CajeroAutomatico()
    cajero.establecer_siguiente(Supervisor()).establecer_siguiente(ComiteRiesgo())

    for monto in [500, 5000, 50000, 500000]:
        transferencia = Transferencia(origen, destino, monto)
        try:
            quien = cajero.aprobar(transferencia)
            print(f"S/. {monto}: aprobada por {quien}")
        except ValueError as error:
            print(f"S/. {monto}: rechazada ({error})")
