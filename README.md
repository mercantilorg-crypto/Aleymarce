# Sistema de Red Bancaria 🏦

Un sistema completo de red bancaria desarrollado en Python que simula operaciones bancarias reales, incluyendo múltiples bancos, clientes, cuentas y transferencias interbancarias.

## 🌟 Características

### Funcionalidades Principales

- **Gestión de Múltiples Bancos**: Crea y administra varios bancos dentro de una red bancaria
- **Gestión de Clientes**: Registro de clientes con información completa
- **Cuentas Bancarias**: 
  - Diferentes tipos de cuentas (Ahorro, Corriente, Inversión)
  - Múltiples cuentas por cliente
  - Balance en tiempo real
- **Operaciones Bancarias**:
  - Depósitos
  - Retiros
  - Transferencias entre cuentas del mismo banco
  - Transferencias interbancarias
- **Historial de Transacciones**: Registro completo de todas las operaciones
- **Estados de Cuenta**: Generación de estados de cuenta detallados
- **Reportes**: Resúmenes financieros por banco y de toda la red

## 🚀 Inicio Rápido

### Requisitos

- Python 3.7 o superior
- No se requieren dependencias externas (solo biblioteca estándar de Python)

### Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd <repository-name>

# El sistema está listo para usar
python demo.py
```

## 📖 Uso

### Ejemplo Básico

```python
from banking_system import BankingNetwork, Bank

# Crear un banco
banco = Bank("Banco Nacional", "BN")

# Registrar un cliente
cliente = banco.register_customer(
    "María García",
    "C001",
    "maria@email.com",
    "555-0001"
)

# Crear una cuenta
cuenta = banco.create_account(cliente, "Ahorro", 1000.0)

# Realizar operaciones
cuenta.deposit(500, "Depósito de nómina")
cuenta.withdraw(200, "Retiro ATM")
cuenta.print_statement()
```

### Transferencias Interbancarias

```python
from banking_system import BankingNetwork, Bank

# Crear red bancaria
red = BankingNetwork("Red Bancaria Nacional")

# Crear bancos
banco1 = Bank("Banco A", "BA")
banco2 = Bank("Banco B", "BB")

# Agregar bancos a la red
red.add_bank(banco1)
red.add_bank(banco2)

# Crear clientes y cuentas en cada banco
cliente1 = banco1.register_customer("Juan", "C1", "juan@email.com", "555-1111")
cuenta1 = banco1.create_account(cliente1, "Ahorro", 5000.0)

cliente2 = banco2.register_customer("Ana", "C2", "ana@email.com", "555-2222")
cuenta2 = banco2.create_account(cliente2, "Ahorro", 3000.0)

# Realizar transferencia interbancaria
red.inter_bank_transfer(
    cuenta1.account_number,
    cuenta2.account_number,
    1000,
    "Pago de servicio"
)

# Ver estado de la red
red.list_banks()
```

## 🎮 Demostraciones

El archivo `demo.py` incluye cuatro demostraciones completas:

1. **Operaciones Básicas**: Muestra depósitos, retiros y transferencias simples
2. **Transferencias Interbancarias**: Demuestra transferencias entre diferentes bancos
3. **Múltiples Cuentas**: Cliente con varias cuentas en el mismo banco
4. **Escenario Completo**: Simulación de un día completo de operaciones bancarias

Para ejecutar las demos:

```bash
python demo.py
```

## 📊 Estructura del Sistema

### Clases Principales

#### `BankingNetwork`
- Coordina múltiples bancos
- Facilita transferencias interbancarias
- Genera reportes consolidados

#### `Bank`
- Gestiona clientes y cuentas
- Genera números de cuenta únicos
- Administra operaciones bancarias

#### `Customer`
- Información del cliente
- Vinculación con múltiples cuentas

#### `Account`
- Gestión de balance
- Historial de transacciones
- Operaciones de depósito, retiro y transferencia

#### `Transaction`
- Registro de todas las operaciones
- Marcas de tiempo
- Trazabilidad completa

## 🔧 Características Técnicas

- **Tipo de Datos**: Uso de enumeraciones para tipos de transacciones
- **UUIDs**: Identificadores únicos para transacciones
- **Timestamps**: Registro de fecha y hora en todas las operaciones
- **Validaciones**: Validación de fondos, montos y existencia de cuentas
- **Formato de Cuenta**: Sistema de numeración `BANCO-XXXXXX`

## 📝 Tipos de Transacciones

- `DEPOSIT`: Depósito en cuenta
- `WITHDRAWAL`: Retiro de cuenta
- `TRANSFER`: Transferencia entre cuentas del mismo banco
- `INTER_BANK_TRANSFER`: Transferencia entre bancos diferentes

## 🛡️ Validaciones

El sistema incluye validaciones para:
- ✅ Fondos suficientes para retiros y transferencias
- ✅ Montos positivos en todas las operaciones
- ✅ Existencia de cuentas y bancos
- ✅ Integridad de datos en transferencias interbancarias

## 📈 Reportes Disponibles

- Estado de cuenta individual
- Lista de cuentas por banco
- Resumen de la red bancaria
- Total de depósitos por banco
- Total consolidado de la red

## 🔮 Posibles Extensiones

- Tasas de interés y cálculo de intereses
- Préstamos y líneas de crédito
- Tarjetas de débito/crédito
- Límites de transacción
- Sistema de autenticación y seguridad
- Comisiones bancarias
- Inversiones y productos financieros
- API REST para integración
- Base de datos persistente
- Interfaz web o móvil

## 👨‍💻 Desarrollo

### Estructura de Archivos

```
/workspace/
├── banking_system.py    # Sistema principal
├── demo.py             # Demostraciones
├── requirements.txt    # Dependencias
└── README.md          # Este archivo
```

### Ejecutar Tests

```bash
# Ejecutar las demos sirve como test básico
python demo.py

# Para tests más exhaustivos, se pueden agregar con pytest
# pytest tests/
```

## 📄 Licencia

Este proyecto está disponible como ejemplo educativo y puede ser usado libremente.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias sobre el sistema de red bancaria, por favor abre un issue en el repositorio.

---

**Nota**: Este es un sistema de demostración para propósitos educativos. No debe ser usado en entornos de producción sin las medidas de seguridad apropiadas.
