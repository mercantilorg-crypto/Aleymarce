# Red Bancaria

Sistema de red bancaria que permite gestionar múltiples bancos, cuentas y realizar transferencias entre ellos.

## Características

- ✅ Gestión de múltiples bancos
- ✅ Gestión de cuentas bancarias
- ✅ Transferencias entre cuentas de diferentes bancos
- ✅ Historial de transacciones
- ✅ API REST completa
- ✅ Validaciones de seguridad (saldo, moneda, estado de cuenta)

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Inicializar la base de datos con datos de ejemplo:
```bash
python init_data.py
```

3. Ejecutar la aplicación:
```bash
python app.py
```

La API estará disponible en `http://localhost:5000`

## API Endpoints

### Bancos

- `GET /api/bancos` - Listar todos los bancos activos
- `POST /api/bancos` - Crear un nuevo banco
- `GET /api/bancos/<id>` - Obtener información de un banco

**Ejemplo crear banco:**
```json
POST /api/bancos
{
  "codigo": "B005",
  "nombre": "Banco Nuevo",
  "pais": "España"
}
```

### Cuentas

- `GET /api/cuentas` - Listar todas las cuentas (opcional: `?banco_id=<id>`)
- `POST /api/cuentas` - Crear una nueva cuenta
- `GET /api/cuentas/<id>` - Obtener información de una cuenta
- `GET /api/cuentas/<id>/saldo` - Obtener saldo de una cuenta

**Ejemplo crear cuenta:**
```json
POST /api/cuentas
{
  "numero_cuenta": "ES0052345678901234567890",
  "banco_id": 1,
  "titular": "Nombre Apellido",
  "saldo": 1000.0,
  "moneda": "USD"
}
```

### Transacciones

- `GET /api/transacciones` - Listar transacciones (opcional: `?cuenta_id=<id>`)
- `POST /api/transacciones` - Crear una nueva transacción/transferencia
- `GET /api/transacciones/<id>` - Obtener información de una transacción

**Ejemplo transferencia:**
```json
POST /api/transacciones
{
  "cuenta_origen_id": 1,
  "cuenta_destino_id": 3,
  "monto": 500.0,
  "tipo": "transferencia",
  "referencia": "TRF-2024-001"
}
```

### Estadísticas

- `GET /api/estadisticas` - Obtener estadísticas de la red bancaria

## Ejemplos de Uso

### Listar bancos
```bash
curl http://localhost:5000/api/bancos
```

### Crear una transferencia
```bash
curl -X POST http://localhost:5000/api/transacciones \
  -H "Content-Type: application/json" \
  -d '{
    "cuenta_origen_id": 1,
    "cuenta_destino_id": 2,
    "monto": 100.0,
    "tipo": "transferencia"
  }'
```

### Obtener estadísticas
```bash
curl http://localhost:5000/api/estadisticas
```

## Estructura del Proyecto

```
.
├── app.py              # Aplicación Flask principal
├── init_data.py        # Script de inicialización de datos
├── requirements.txt    # Dependencias del proyecto
├── README.md          # Documentación
└── banking_network.db # Base de datos SQLite (se crea automáticamente)
```

## Modelos de Datos

### Banco
- `id`: Identificador único
- `codigo`: Código único del banco
- `nombre`: Nombre del banco
- `pais`: País donde opera
- `activo`: Estado activo/inactivo

### Cuenta
- `id`: Identificador único
- `numero_cuenta`: Número de cuenta único
- `banco_id`: ID del banco al que pertenece
- `titular`: Nombre del titular
- `saldo`: Saldo actual
- `moneda`: Moneda de la cuenta (USD, EUR, etc.)
- `activa`: Estado activa/inactiva

### Transaccion
- `id`: Identificador único
- `cuenta_origen_id`: ID de la cuenta origen
- `cuenta_destino_id`: ID de la cuenta destino
- `monto`: Monto de la transacción
- `moneda`: Moneda de la transacción
- `tipo`: Tipo de transacción
- `estado`: Estado (pendiente, completada, rechazada)
- `referencia`: Referencia única de la transacción

## Validaciones

- Las transferencias requieren saldo suficiente en la cuenta origen
- Las cuentas deben tener la misma moneda para transferir
- Solo se pueden realizar transferencias entre cuentas activas
- Las transacciones se procesan automáticamente al crearse

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y de desarrollo.
