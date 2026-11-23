from datetime import datetime

class RegistroAuditoria:
    """ guarda un historial de cada operación, aprobada o rechazada"""

    def __init__(self):
        self._eventos = []

    def registrar(self, estado, detalle):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._eventos.append({"fecha": fecha, "estado": estado, "detalle": detalle})

    def eventos(self):
        """ devuelve una copia de la lista, para que nadie la altere por fuera"""
        return list(self._eventos)

    def mostrar(self):
        if not self._eventos:
            print("Sin operaciones registradas")
            return
        for evento in self._eventos:
            print(f"[{evento['fecha']}] {evento['estado']}: {evento['detalle']}")
