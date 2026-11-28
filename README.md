# sistema-banca-dp
El proyecto final del curso **Diseño de Patrones** (UTP), proyecto 7.
Aplicación de consola en **Python** que simula un banco digital: el cliente consulta su saldo y hace transferencias, y el sistema valida, calcula la comisión, pide aprobación según el monto, exige un código de verificación (2FA) y deja un historial de auditoría.

## Patrones de diseño aplicados

- **Builder** (`transferencia.py`): arma la transferencia paso a paso y la valida antes de crearla.
- **Strategy** (`comisiones.py`): calcula la comisión según el tipo de cuenta, sin `if/else`.
- **Chain of Responsibility** (`aprobacion.py`): la transferencia pasa de aprobador en aprobador hasta que alguien puede aprobarla por su monto.
- **Proxy** (`ejecucion.py`): se pone delante del ejecutor real y pide el 2FA antes de mover el dinero.

## Requisitos

- Python 3 (no necesita instalar ninguna librería externa).
- Cualquier sistema operativo. Probado en Windows con Visual Studio Code.

## Instalación

1. Clona el repositorio (o descarga el ZIP desde GitHub y descomprímelo):
   ```
   git clone https://github.com/DAY-20/sistema-banca-dp.git
   cd sistema-banca-dp
   ```
2. Comprueba que tienes Python:
   ```
   python --version
   ```
No hay nada más que instalar.

## Cómo usar el sistema

Ejecuta el menú:
```
python menu.py
```
Al empezar, el sistema pide el nombre del titular. Las cuentas de prueba son:

| Titular | Tipo de cuenta | Saldo inicial |
| Dayanna | Corriente      | S/ 2,000      |
| Bry     | Ahorros        | S/ 500        |
| Vali    | Corriente      | S/ 150,000    |

Puedes escribir `salir` en lugar del nombre para cerrar el programa.

Después aparece el menú del cliente:

| Opción | Qué hace                   |
| 1      | Consultar saldo            |
| 2      | Hacer transferencia        |
| 3      | Ver historial de auditoría |
| 4      | Cambiar de usuario         |
| 5      | Salir                      |

### Cómo hacer una transferencia

1. Elige la opción **2**.
2. Escribe el titular de la cuenta destino (por ejemplo, `Bry`).
3. Escribe el monto.
4. El sistema muestra un resumen con la comisión y el total.
5. Se pide el **2FA**: en pantalla aparece un código de 6 dígitos como "SMS simulado". Escríbelo para confirmar.
6. Si todo sale bien, verás quién aprobó la transferencia. Si algo falla, verás un mensaje claro y el programa sigue funcionando.

### Reglas del sistema

**Comisión** (patrón Strategy), según el tipo de cuenta de origen:

| Cuenta origen | Comisión      |
| Ahorros       | 1 % del monto |
| Corriente     | S/ 5 fijos    |

**Aprobación** (patrón Chain of Responsibility), según el monto:

| Monto             | Quién aprueba     |
| Hasta S/ 1,000    | Cajero automático |
| Hasta S/ 10,000   | Supervisor        |
| Hasta S/ 100,000  | Comité de riesgo  |
| Más de S/ 100,000 | Se rechaza        |

La aprobación se decide con el **monto** de la transferencia, sin sumar la comisión.

**Validaciones:** el monto debe ser mayor a cero, la cuenta destino debe existir y ser distinta de la origen, y el saldo debe alcanzar para el monto más la comisión.

## Estructura del proyecto

```
sistema-banca-dp/
├── cuenta.py            Cuenta, CuentaAhorros y CuentaCorriente
├── comisiones.py        Strategy: EstrategiaComision y sus dos comisiones
├── transferencia.py     Builder: Transferencia y TransferenciaBuilder
├── aprobacion.py        Chain of Responsibility: Aprobador y sus tres niveles
├── ejecucion.py         Proxy: EjecutorTransferencia, EjecutorReal y ProxyAutenticacion
├── auditoria.py         RegistroAuditoria (historial; no es un patrón)
├── servicio.py          ServicioTransferencias: coordina aprobar, ejecutar y registrar
├── menu.py              Menú de consola (punto de entrada)
├── test_sistema.py      Pruebas automáticas con unittest
└── docs/                Diagramas UML
```

### Cómo se conectan las piezas

1. `menu.py` pide los datos al cliente y arma la transferencia con el **Builder**, que usa una **Strategy** para calcular la comisión.
2. `ServicioTransferencias` recibe la transferencia y la pasa por la **cadena de aprobación**.
3. Si alguien la aprueba, el servicio la manda al **Proxy**, que pide el 2FA y solo entonces llama al ejecutor real.
4. El servicio anota el resultado (APROBADA o RECHAZADA) en la **auditoría**.

## Diagramas UML

Están en la carpeta `docs/`:

- Diagrama de clases: `docs/patron_completo.png`
- Diagrama de secuencia: `docs/diagrama_secuencia.png`
- Diagrama de actividad: `docs/diagrama_actividada.png`

## Pruebas

El proyecto tiene 10 pruebas automáticas que validan los cuatro patrones y la integración con la auditoría. Para correrlas:

```
python -m unittest test_sistema -v
```

Si todo está bien, el final de la salida dice `OK`. Durante las pruebas del Proxy se imprime un código 2FA de ejemplo; es normal.

## Decisiones de diseño

- **Sin contraseña de inicio de sesión:** la seguridad de la operación la da el 2FA del Proxy. Tampoco se pueden crear cuentas nuevas.
- **Los datos viven en memoria:** al cerrar el programa, los saldos y el historial se reinician. No hay base de datos.
- **Auditoría:** se registra cada transferencia que llega a la etapa de aprobación, aprobada o rechazada. Los errores de validación previos (por ejemplo, saldo insuficiente) solo se muestran en pantalla.
- **Historial compartido:** la opción 3 muestra las operaciones de todos los usuarios.

## Mejoras futuras

- Guardar cuentas y auditoría en una base de datos.
- Comisión según la moneda (soles y dólares).
- Pago de servicios (luz, agua).
- Registrar también los errores de validación en la auditoría.
- Historial de auditoría separado por usuario.

## Autora
Dayanna Taboada :3
