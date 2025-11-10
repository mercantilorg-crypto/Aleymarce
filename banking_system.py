"""
Sistema de Red Bancaria
A comprehensive banking network system with support for multiple banks,
accounts, customers, and inter-bank transfers.
"""

from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
import uuid


class TransactionType(Enum):
    """Tipos de transacciones"""
    DEPOSIT = "Depósito"
    WITHDRAWAL = "Retiro"
    TRANSFER = "Transferencia"
    INTER_BANK_TRANSFER = "Transferencia Interbancaria"


class Transaction:
    """Representa una transacción bancaria"""
    
    def __init__(self, transaction_type: TransactionType, amount: float, 
                 from_account: Optional[str] = None, to_account: Optional[str] = None,
                 description: str = ""):
        self.id = str(uuid.uuid4())
        self.transaction_type = transaction_type
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.description = description
        self.timestamp = datetime.now()
        
    def __str__(self):
        return (f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{self.transaction_type.value}: ${self.amount:.2f} - {self.description}")


class Customer:
    """Representa un cliente del banco"""
    
    def __init__(self, name: str, customer_id: str, email: str, phone: str):
        self.name = name
        self.customer_id = customer_id
        self.email = email
        self.phone = phone
        self.accounts: List['Account'] = []
        
    def add_account(self, account: 'Account'):
        """Agrega una cuenta al cliente"""
        self.accounts.append(account)
        
    def __str__(self):
        return f"Cliente: {self.name} (ID: {self.customer_id})"


class Account:
    """Representa una cuenta bancaria"""
    
    def __init__(self, account_number: str, customer: Customer, 
                 account_type: str = "Ahorro", initial_balance: float = 0.0):
        self.account_number = account_number
        self.customer = customer
        self.account_type = account_type
        self.balance = initial_balance
        self.transactions: List[Transaction] = []
        self.is_active = True
        self.created_at = datetime.now()
        
        # Agregar cuenta al cliente
        customer.add_account(self)
        
    def deposit(self, amount: float, description: str = "Depósito") -> bool:
        """Realiza un depósito en la cuenta"""
        if amount <= 0:
            print(f"Error: El monto debe ser mayor a 0")
            return False
            
        self.balance += amount
        transaction = Transaction(
            TransactionType.DEPOSIT, 
            amount, 
            to_account=self.account_number,
            description=description
        )
        self.transactions.append(transaction)
        print(f"✓ Depósito exitoso: ${amount:.2f}. Nuevo balance: ${self.balance:.2f}")
        return True
        
    def withdraw(self, amount: float, description: str = "Retiro") -> bool:
        """Realiza un retiro de la cuenta"""
        if amount <= 0:
            print(f"Error: El monto debe ser mayor a 0")
            return False
            
        if amount > self.balance:
            print(f"Error: Fondos insuficientes. Balance actual: ${self.balance:.2f}")
            return False
            
        self.balance -= amount
        transaction = Transaction(
            TransactionType.WITHDRAWAL, 
            amount, 
            from_account=self.account_number,
            description=description
        )
        self.transactions.append(transaction)
        print(f"✓ Retiro exitoso: ${amount:.2f}. Nuevo balance: ${self.balance:.2f}")
        return True
        
    def transfer(self, to_account: 'Account', amount: float, 
                 description: str = "Transferencia") -> bool:
        """Transfiere dinero a otra cuenta"""
        if amount <= 0:
            print(f"Error: El monto debe ser mayor a 0")
            return False
            
        if amount > self.balance:
            print(f"Error: Fondos insuficientes. Balance actual: ${self.balance:.2f}")
            return False
            
        # Retirar de cuenta origen
        self.balance -= amount
        transaction_out = Transaction(
            TransactionType.TRANSFER, 
            amount, 
            from_account=self.account_number,
            to_account=to_account.account_number,
            description=f"{description} a {to_account.account_number}"
        )
        self.transactions.append(transaction_out)
        
        # Depositar en cuenta destino
        to_account.balance += amount
        transaction_in = Transaction(
            TransactionType.TRANSFER, 
            amount, 
            from_account=self.account_number,
            to_account=to_account.account_number,
            description=f"{description} de {self.account_number}"
        )
        to_account.transactions.append(transaction_in)
        
        print(f"✓ Transferencia exitosa: ${amount:.2f} a cuenta {to_account.account_number}")
        return True
        
    def get_balance(self) -> float:
        """Retorna el balance actual"""
        return self.balance
        
    def get_transaction_history(self, limit: int = 10) -> List[Transaction]:
        """Retorna el historial de transacciones"""
        return self.transactions[-limit:]
        
    def print_statement(self):
        """Imprime un estado de cuenta"""
        print(f"\n{'='*60}")
        print(f"ESTADO DE CUENTA")
        print(f"{'='*60}")
        print(f"Número de Cuenta: {self.account_number}")
        print(f"Titular: {self.customer.name}")
        print(f"Tipo de Cuenta: {self.account_type}")
        print(f"Balance Actual: ${self.balance:.2f}")
        print(f"Estado: {'Activa' if self.is_active else 'Inactiva'}")
        print(f"\nÚltimas Transacciones:")
        print(f"{'-'*60}")
        
        recent_transactions = self.get_transaction_history(10)
        if not recent_transactions:
            print("No hay transacciones registradas")
        else:
            for trans in recent_transactions:
                print(trans)
        print(f"{'='*60}\n")
        
    def __str__(self):
        return f"Cuenta {self.account_number} - {self.account_type} (Balance: ${self.balance:.2f})"


class Bank:
    """Representa un banco en la red bancaria"""
    
    def __init__(self, bank_name: str, bank_code: str):
        self.bank_name = bank_name
        self.bank_code = bank_code
        self.customers: Dict[str, Customer] = {}
        self.accounts: Dict[str, Account] = {}
        self.account_counter = 1000
        
    def register_customer(self, name: str, customer_id: str, 
                         email: str, phone: str) -> Customer:
        """Registra un nuevo cliente"""
        if customer_id in self.customers:
            print(f"Error: Cliente con ID {customer_id} ya existe")
            return self.customers[customer_id]
            
        customer = Customer(name, customer_id, email, phone)
        self.customers[customer_id] = customer
        print(f"✓ Cliente registrado: {customer.name}")
        return customer
        
    def create_account(self, customer: Customer, account_type: str = "Ahorro", 
                       initial_balance: float = 0.0) -> Account:
        """Crea una nueva cuenta bancaria"""
        account_number = f"{self.bank_code}-{self.account_counter:06d}"
        self.account_counter += 1
        
        account = Account(account_number, customer, account_type, initial_balance)
        self.accounts[account_number] = account
        print(f"✓ Cuenta creada: {account_number} para {customer.name}")
        return account
        
    def get_account(self, account_number: str) -> Optional[Account]:
        """Obtiene una cuenta por su número"""
        return self.accounts.get(account_number)
        
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Obtiene un cliente por su ID"""
        return self.customers.get(customer_id)
        
    def list_accounts(self):
        """Lista todas las cuentas del banco"""
        print(f"\n{'='*60}")
        print(f"CUENTAS DE {self.bank_name}")
        print(f"{'='*60}")
        if not self.accounts:
            print("No hay cuentas registradas")
        else:
            for account_number, account in self.accounts.items():
                print(f"{account} - Titular: {account.customer.name}")
        print(f"{'='*60}\n")
        
    def get_total_deposits(self) -> float:
        """Calcula el total de depósitos en el banco"""
        return sum(account.balance for account in self.accounts.values())
        
    def __str__(self):
        return f"{self.bank_name} (Código: {self.bank_code})"


class BankingNetwork:
    """Red bancaria que coordina múltiples bancos"""
    
    def __init__(self, network_name: str):
        self.network_name = network_name
        self.banks: Dict[str, Bank] = {}
        
    def add_bank(self, bank: Bank):
        """Agrega un banco a la red"""
        if bank.bank_code in self.banks:
            print(f"Error: Banco con código {bank.bank_code} ya existe en la red")
            return
            
        self.banks[bank.bank_code] = bank
        print(f"✓ Banco agregado a la red: {bank.bank_name}")
        
    def get_bank(self, bank_code: str) -> Optional[Bank]:
        """Obtiene un banco por su código"""
        return self.banks.get(bank_code)
        
    def inter_bank_transfer(self, from_account_number: str, 
                           to_account_number: str, amount: float,
                           description: str = "Transferencia Interbancaria") -> bool:
        """Realiza una transferencia entre cuentas de diferentes bancos"""
        
        # Extraer códigos de banco de los números de cuenta
        from_bank_code = from_account_number.split('-')[0]
        to_bank_code = to_account_number.split('-')[0]
        
        # Obtener bancos
        from_bank = self.get_bank(from_bank_code)
        to_bank = self.get_bank(to_bank_code)
        
        if not from_bank:
            print(f"Error: Banco origen {from_bank_code} no encontrado en la red")
            return False
            
        if not to_bank:
            print(f"Error: Banco destino {to_bank_code} no encontrado en la red")
            return False
            
        # Obtener cuentas
        from_account = from_bank.get_account(from_account_number)
        to_account = to_bank.get_account(to_account_number)
        
        if not from_account:
            print(f"Error: Cuenta origen {from_account_number} no encontrada")
            return False
            
        if not to_account:
            print(f"Error: Cuenta destino {to_account_number} no encontrada")
            return False
            
        # Realizar transferencia
        if amount <= 0:
            print(f"Error: El monto debe ser mayor a 0")
            return False
            
        if amount > from_account.balance:
            print(f"Error: Fondos insuficientes. Balance actual: ${from_account.balance:.2f}")
            return False
            
        # Retirar de cuenta origen
        from_account.balance -= amount
        transaction_out = Transaction(
            TransactionType.INTER_BANK_TRANSFER, 
            amount, 
            from_account=from_account_number,
            to_account=to_account_number,
            description=f"{description} a {to_bank.bank_name}"
        )
        from_account.transactions.append(transaction_out)
        
        # Depositar en cuenta destino
        to_account.balance += amount
        transaction_in = Transaction(
            TransactionType.INTER_BANK_TRANSFER, 
            amount, 
            from_account=from_account_number,
            to_account=to_account_number,
            description=f"{description} de {from_bank.bank_name}"
        )
        to_account.transactions.append(transaction_in)
        
        print(f"✓ Transferencia interbancaria exitosa: ${amount:.2f}")
        print(f"  De: {from_bank.bank_name} ({from_account_number})")
        print(f"  A: {to_bank.bank_name} ({to_account_number})")
        return True
        
    def list_banks(self):
        """Lista todos los bancos en la red"""
        print(f"\n{'='*60}")
        print(f"RED BANCARIA: {self.network_name}")
        print(f"{'='*60}")
        if not self.banks:
            print("No hay bancos registrados en la red")
        else:
            for bank_code, bank in self.banks.items():
                total_deposits = bank.get_total_deposits()
                print(f"{bank} - Cuentas: {len(bank.accounts)} - Total Depósitos: ${total_deposits:.2f}")
        print(f"{'='*60}\n")
        
    def get_network_total(self) -> float:
        """Calcula el total de dinero en toda la red bancaria"""
        return sum(bank.get_total_deposits() for bank in self.banks.values())
        
    def __str__(self):
        return f"Red Bancaria: {self.network_name} ({len(self.banks)} bancos)"
