#!/usr/bin/env python3
"""
Demo del Sistema de Red Bancaria
Demuestra las capacidades del sistema bancario
"""

from banking_system import BankingNetwork, Bank, Customer, Account


def print_header(title: str):
    """Imprime un encabezado formateado"""
    print(f"\n{'#'*70}")
    print(f"# {title}")
    print(f"{'#'*70}\n")


def demo_basic_operations():
    """Demuestra operaciones básicas de un banco"""
    print_header("DEMO 1: Operaciones Básicas de un Banco")
    
    # Crear un banco
    banco_nacional = Bank("Banco Nacional", "BN")
    
    # Registrar clientes
    cliente1 = banco_nacional.register_customer(
        "María García", 
        "C001", 
        "maria@email.com", 
        "555-0001"
    )
    
    cliente2 = banco_nacional.register_customer(
        "Juan Pérez", 
        "C002", 
        "juan@email.com", 
        "555-0002"
    )
    
    # Crear cuentas
    cuenta_maria = banco_nacional.create_account(cliente1, "Ahorro", 1000.0)
    cuenta_juan = banco_nacional.create_account(cliente2, "Corriente", 500.0)
    
    # Operaciones
    print("\n--- Operaciones Bancarias ---")
    cuenta_maria.deposit(500, "Depósito inicial")
    cuenta_maria.withdraw(200, "Retiro ATM")
    cuenta_maria.transfer(cuenta_juan, 300, "Pago servicios")
    
    # Estados de cuenta
    cuenta_maria.print_statement()
    cuenta_juan.print_statement()
    
    # Listar cuentas
    banco_nacional.list_accounts()


def demo_inter_bank_transfers():
    """Demuestra transferencias interbancarias"""
    print_header("DEMO 2: Transferencias Interbancarias")
    
    # Crear red bancaria
    red = BankingNetwork("Red Bancaria Nacional")
    
    # Crear múltiples bancos
    banco_popular = Bank("Banco Popular", "BP")
    banco_comercio = Bank("Banco de Comercio", "BC")
    banco_ahorro = Bank("Banco de Ahorro", "BA")
    
    # Agregar bancos a la red
    red.add_bank(banco_popular)
    red.add_bank(banco_comercio)
    red.add_bank(banco_ahorro)
    
    # Registrar clientes en diferentes bancos
    cliente_bp = banco_popular.register_customer(
        "Ana López", "C101", "ana@email.com", "555-1001"
    )
    cliente_bc = banco_comercio.register_customer(
        "Carlos Ruiz", "C102", "carlos@email.com", "555-1002"
    )
    cliente_ba = banco_ahorro.register_customer(
        "Laura Martínez", "C103", "laura@email.com", "555-1003"
    )
    
    # Crear cuentas en diferentes bancos
    cuenta_bp = banco_popular.create_account(cliente_bp, "Ahorro", 5000.0)
    cuenta_bc = banco_comercio.create_account(cliente_bc, "Corriente", 3000.0)
    cuenta_ba = banco_ahorro.create_account(cliente_ba, "Ahorro", 2000.0)
    
    # Listar red bancaria
    red.list_banks()
    
    # Realizar transferencias interbancarias
    print("\n--- Transferencias Interbancarias ---")
    red.inter_bank_transfer(
        cuenta_bp.account_number, 
        cuenta_bc.account_number, 
        1000, 
        "Pago de factura"
    )
    
    red.inter_bank_transfer(
        cuenta_bc.account_number, 
        cuenta_ba.account_number, 
        500, 
        "Ahorro mensual"
    )
    
    # Estados de cuenta después de transferencias
    cuenta_bp.print_statement()
    cuenta_bc.print_statement()
    cuenta_ba.print_statement()
    
    # Resumen de la red
    red.list_banks()
    total_network = red.get_network_total()
    print(f"\n💰 Total en la Red Bancaria: ${total_network:.2f}\n")


def demo_multiple_accounts():
    """Demuestra cliente con múltiples cuentas"""
    print_header("DEMO 3: Cliente con Múltiples Cuentas")
    
    # Crear banco
    banco = Bank("Banco Universal", "BU")
    
    # Registrar cliente
    cliente = banco.register_customer(
        "Roberto Sánchez", 
        "C201", 
        "roberto@email.com", 
        "555-2001"
    )
    
    # Crear múltiples cuentas para el mismo cliente
    cuenta_ahorro = banco.create_account(cliente, "Ahorro", 10000.0)
    cuenta_corriente = banco.create_account(cliente, "Corriente", 2000.0)
    cuenta_inversion = banco.create_account(cliente, "Inversión", 50000.0)
    
    print(f"\n{cliente}")
    print(f"Número de cuentas: {len(cliente.accounts)}")
    print("\nCuentas del cliente:")
    for cuenta in cliente.accounts:
        print(f"  - {cuenta}")
    
    # Operaciones entre cuentas del mismo cliente
    print("\n--- Movimientos entre Cuentas ---")
    cuenta_ahorro.transfer(cuenta_corriente, 1000, "Transferencia personal")
    cuenta_inversion.withdraw(5000, "Retiro para inversión externa")
    cuenta_ahorro.deposit(3000, "Depósito de nómina")
    
    # Estados de cuenta
    for cuenta in cliente.accounts:
        cuenta.print_statement()
    
    # Total del cliente
    total_cliente = sum(cuenta.balance for cuenta in cliente.accounts)
    print(f"\n💰 Total del Cliente: ${total_cliente:.2f}\n")


def demo_comprehensive_scenario():
    """Demuestra un escenario completo con múltiples operaciones"""
    print_header("DEMO 4: Escenario Completo")
    
    # Crear red bancaria
    red = BankingNetwork("Sistema Bancario Integrado")
    
    # Crear bancos
    bancos = {
        "BCN": Bank("Banco Central Nacional", "BCN"),
        "BIP": Bank("Banco Internacional Premium", "BIP"),
        "BPY": Bank("Banco del Pueblo y Ahorro", "BPY")
    }
    
    for banco in bancos.values():
        red.add_bank(banco)
    
    # Crear varios clientes y cuentas
    clientes_datos = [
        ("BCN", "Elena Torres", "C301", "elena@email.com", "555-3001", 15000),
        ("BCN", "Miguel Ángel", "C302", "miguel@email.com", "555-3002", 8000),
        ("BIP", "Sofia Ramírez", "C303", "sofia@email.com", "555-3003", 25000),
        ("BIP", "Diego Castro", "C304", "diego@email.com", "555-3004", 12000),
        ("BPY", "Carmen Flores", "C305", "carmen@email.com", "555-3005", 6000),
        ("BPY", "Ricardo Vega", "C306", "ricardo@email.com", "555-3006", 9000),
    ]
    
    cuentas = {}
    for banco_code, nombre, cust_id, email, phone, balance in clientes_datos:
        banco = bancos[banco_code]
        cliente = banco.register_customer(nombre, cust_id, email, phone)
        cuenta = banco.create_account(cliente, "Ahorro", balance)
        cuentas[cust_id] = cuenta
    
    print("\n--- Estado Inicial de la Red ---")
    red.list_banks()
    
    # Simular un día de operaciones
    print("\n--- Simulación de Operaciones Diarias ---")
    
    # Depósitos
    cuentas["C301"].deposit(2000, "Pago de cliente")
    cuentas["C305"].deposit(1500, "Depósito de nómina")
    
    # Retiros
    cuentas["C302"].withdraw(500, "Retiro ATM")
    cuentas["C304"].withdraw(1000, "Pago en efectivo")
    
    # Transferencias internas
    cuentas["C301"].transfer(cuentas["C302"], 1000, "Pago préstamo")
    
    # Transferencias interbancarias
    red.inter_bank_transfer(
        cuentas["C303"].account_number,
        cuentas["C305"].account_number,
        3000,
        "Transferencia familiar"
    )
    
    red.inter_bank_transfer(
        cuentas["C306"].account_number,
        cuentas["C304"].account_number,
        2000,
        "Pago de servicio"
    )
    
    # Estado final
    print("\n--- Estado Final de la Red ---")
    red.list_banks()
    
    print(f"\n{'='*70}")
    print(f"💰 RESUMEN TOTAL")
    print(f"{'='*70}")
    print(f"Total en la Red Bancaria: ${red.get_network_total():.2f}")
    print(f"Número de Bancos: {len(red.banks)}")
    total_cuentas = sum(len(banco.accounts) for banco in red.banks.values())
    print(f"Total de Cuentas: {total_cuentas}")
    total_clientes = sum(len(banco.customers) for banco in red.banks.values())
    print(f"Total de Clientes: {total_clientes}")
    print(f"{'='*70}\n")


def main():
    """Ejecuta todas las demos"""
    print("\n" + "="*70)
    print("  SISTEMA DE RED BANCARIA - DEMOSTRACIONES")
    print("="*70)
    
    try:
        # Ejecutar demos
        demo_basic_operations()
        input("\nPresiona Enter para continuar a la siguiente demo...")
        
        demo_inter_bank_transfers()
        input("\nPresiona Enter para continuar a la siguiente demo...")
        
        demo_multiple_accounts()
        input("\nPresiona Enter para continuar a la siguiente demo...")
        
        demo_comprehensive_scenario()
        
        print("\n✓ Todas las demostraciones completadas exitosamente!")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
