import unittest

from cuenta import CuentaAhorros, CuentaCorriente
from comisiones import ComisionAhorros, ComisionCorriente
from transferencia import TransferenciaBuilder
from aprobacion import Aprobador, CajeroAutomatico, Supervisor, ComiteRiesgo
from ejecucion import EjecutorReal, ProxyAutenticacion
from auditoria import RegistroAuditoria
from servicio import ServicioTransferencias

def crear_cadena():
    """ la cadena de aprobación: cajero -> supervisor -> comité de riesgo"""
    cajero = CajeroAutomatico()
    cajero.establecer_siguiente(Supervisor()).establecer_siguiente(ComiteRiesgo())
    return cajero

def crear_proxy(codigo_que_escribe_el_cliente):
    """ proxy de prueba: el código correcto siempre es 123456 y el cliente
    'escribe' el que le indiquemos, sin usar input()."""
    return ProxyAutenticacion(
        EjecutorReal(),
        pedir_codigo=lambda mensaje: codigo_que_escribe_el_cliente,
        generar_codigo=lambda: "123456",
    )

class PruebasBuilder(unittest.TestCase):
    """ patrón builder: arma y valida la transferencia"""
    def setUp(self):
        self.origen = CuentaCorriente("Dayanna", 1000)
        self.destino = CuentaAhorros("Bry", 500)

    def test_construye_una_transferencia_valida(self):
        transferencia = (TransferenciaBuilder()
                         .con_origen(self.origen)
                         .con_destino(self.destino)
                         .con_monto(300)
                         .con_comision(ComisionCorriente())
                         .construir())
        self.assertEqual(transferencia.monto, 300)
        self.assertEqual(transferencia.comision, 5)
        self.assertEqual(transferencia.total, 305)

    def test_rechaza_datos_invalidos(self):
        casos = [
            ("monto negativo", self.destino, -10),
            ("misma cuenta", self.origen, 100),
            ("saldo insuficiente", self.destino, 5000),
        ]
        for descripcion, destino, monto in casos:
            with self.subTest(descripcion):
                with self.assertRaises(ValueError):
                    (TransferenciaBuilder()
                     .con_origen(self.origen)
                     .con_destino(destino)
                     .con_monto(monto)
                     .construir())
                    
class PruebasStrategy(unittest.TestCase):
    """ patrón strategy: la comisión cambia según la estrategia"""

    def test_cada_estrategia_calcula_su_comision(self):
        self.assertEqual(ComisionAhorros().calcular(300), 3.0)
        self.assertEqual(ComisionCorriente().calcular(300), 5.0)

    def test_el_builder_usa_la_estrategia_que_recibe(self):
        origen = CuentaCorriente("Dayanna", 1000)
        destino = CuentaAhorros("Bry", 500)
        transferencia = (TransferenciaBuilder()
                         .con_origen(origen)
                         .con_destino(destino)
                         .con_monto(200)
                         .con_comision(ComisionAhorros())
                         .construir())
        self.assertEqual(transferencia.comision, 2.0)

class PruebasChain(unittest.TestCase):
    """patrón chain of responsibility: aprueba quien tenga el límite"""
    def aprobador_para(self, monto):
        origen = CuentaCorriente("Dayanna", 1000000)
        destino = CuentaAhorros("Bry", 0)
        transferencia = (TransferenciaBuilder()
                         .con_origen(origen)
                         .con_destino(destino)
                         .con_monto(monto)
                         .construir())
        return crear_cadena().aprobar(transferencia)

    def test_aprueba_quien_corresponde_segun_el_monto(self):
        self.assertEqual(self.aprobador_para(500), "Cajero automático")
        self.assertEqual(self.aprobador_para(5000), "Supervisor")
        self.assertEqual(self.aprobador_para(50000), "Comité de riesgo")

    def test_rechaza_si_supera_todos_los_limites(self):
        with self.assertRaises(ValueError):
            self.aprobador_para(500000)

    def test_se_puede_agregar_un_aprobador_sin_modificar_los_existentes(self):
        class Gerente(Aprobador):
            nombre = "Gerente"
            def puede_aprobar(self, transferencia):
                return transferencia.monto <= 50000

        cajero = CajeroAutomatico()
        cajero.establecer_siguiente(Supervisor()).establecer_siguiente(
            Gerente()).establecer_siguiente(ComiteRiesgo())

        origen = CuentaCorriente("Dayanna", 1000000)
        destino = CuentaAhorros("Bry", 0)
        transferencia = (TransferenciaBuilder()
                         .con_origen(origen)
                         .con_destino(destino)
                         .con_monto(30000)
                         .construir())
        self.assertEqual(cajero.aprobar(transferencia), "Gerente")

class PruebasProxy(unittest.TestCase):
    """patrón proxy: el 2FA protege la ejecución real"""
    def setUp(self):
        self.origen = CuentaCorriente("Dayanna", 1000)
        self.destino = CuentaAhorros("Bry", 500)
        self.transferencia = (TransferenciaBuilder()
                              .con_origen(self.origen)
                              .con_destino(self.destino)
                              .con_monto(300)
                              .con_comision(ComisionCorriente())
                              .construir())

    def test_con_codigo_correcto_mueve_el_dinero(self):
        crear_proxy("123456").ejecutar(self.transferencia)
        self.assertEqual(self.origen.saldo, 695)
        self.assertEqual(self.destino.saldo, 800)

    def test_con_codigo_incorrecto_bloquea_y_no_mueve_dinero(self):
        with self.assertRaises(PermissionError):
            crear_proxy("000000").ejecutar(self.transferencia)
        self.assertEqual(self.origen.saldo, 1000)
        self.assertEqual(self.destino.saldo, 500)

class PruebasServicio(unittest.TestCase):
    """Se integran: la aprobación + 2FA + auditoría trabajando juntas"""

    def test_registra_operaciones_aprobadas_y_rechazadas(self):
        origen = CuentaCorriente("Dayanna", 1000)
        destino = CuentaAhorros("Bry", 500)
        auditoria = RegistroAuditoria()

        def nueva_transferencia():
            return (TransferenciaBuilder()
                    .con_origen(origen)
                    .con_destino(destino)
                    .con_monto(100)
                    .con_comision(ComisionCorriente())
                    .construir())

        servicio_ok = ServicioTransferencias(
            crear_cadena(), crear_proxy("123456"), auditoria)
        servicio_ok.transferir(nueva_transferencia())

        servicio_mal = ServicioTransferencias(
            crear_cadena(), crear_proxy("000000"), auditoria)
        with self.assertRaises(PermissionError):
            servicio_mal.transferir(nueva_transferencia())

        estados = [evento["estado"] for evento in auditoria.eventos()]
        self.assertEqual(estados, ["APROBADA", "RECHAZADA"])

if __name__ == "__main__":
    unittest.main()