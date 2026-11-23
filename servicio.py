class ServicioTransferencias:
    """ coordina el flujo: aprobar, ejecutar (con 2FA) y registra"""
    def __init__(self, primer_aprobador, ejecutor, auditoria):
        self._primer_aprobador = primer_aprobador
        self._ejecutor = ejecutor
        self._auditoria = auditoria

    def transferir(self, transferencia):
        """ devuelve quién aprobó, si algo falla, lo registra y relanza el error"""
        try:
            aprobador = self._primer_aprobador.aprobar(transferencia)
            self._ejecutor.ejecutar(transferencia)
            self._auditoria.registrar(
                "APROBADA", f"{transferencia} | aprobada por {aprobador}")
            return aprobador
        except (ValueError, PermissionError) as error:
            self._auditoria.registrar(
                "RECHAZADA", f"{transferencia} | motivo: {error}")
            raise
# Prueba
if __name__ == "__main__":
    from cuenta import CuentaAhorros, CuentaCorriente
    from comisiones import ComisionCorriente
    from transferencia import TransferenciaBuilder
    from aprobacion import CajeroAutomatico, Supervisor, ComiteRiesgo
    from ejecucion import EjecutorReal, ProxyAutenticacion
    from auditoria import RegistroAuditoria

    bry = CuentaAhorros("Bry", 500)
    dayanna = CuentaCorriente("Dayanna", 1000000)

    cajero = CajeroAutomatico()
    cajero.establecer_siguiente(Supervisor()).establecer_siguiente(ComiteRiesgo())
    auditoria = RegistroAuditoria()

    def proxy_con_codigo(codigo_cliente):
        """proxy de prueba, el código se escribe solo, sin input()"""
        return ProxyAutenticacion(EjecutorReal(),
                                  pedir_codigo=lambda mensaje: codigo_cliente,
                                  generar_codigo=lambda: "123456")

    # (descripción, monto, código que "escribe" el cliente)
    casos = [
        ("Monto bajo, código correcto", 300, "123456"),
        ("Código incorrecto", 300, "000000"),
        ("Monto medio, código correcto", 5000, "123456"),
        ("Monto enorme", 500000, "123456"),
    ]

    for descripcion, monto, codigo_cliente in casos:
        servicio = ServicioTransferencias(
            cajero, proxy_con_codigo(codigo_cliente), auditoria)
        try:
            transferencia = (TransferenciaBuilder()
                             .con_origen(dayanna)
                             .con_destino(bry)
                             .con_monto(monto)
                             .con_comision(ComisionCorriente())
                             .construir())
            quien = servicio.transferir(transferencia)
            print(f"{descripcion}: aprobada por {quien}")
        except (ValueError, PermissionError) as error:
            print(f"{descripcion}: rechazada ({error})")

    print()
    dayanna.mostrar_saldo()
    bry.mostrar_saldo()
    print()
    auditoria.mostrar()
