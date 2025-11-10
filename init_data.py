"""
Script para inicializar la base de datos con datos de ejemplo
"""
from app import app, db, Banco, Cuenta
from datetime import datetime

def inicializar_datos():
    with app.app_context():
        # Limpiar datos existentes (opcional)
        db.drop_all()
        db.create_all()
        
        # Crear bancos
        bancos_data = [
            {'codigo': 'B001', 'nombre': 'Banco Nacional', 'pais': 'España'},
            {'codigo': 'B002', 'nombre': 'Banco Internacional', 'pais': 'España'},
            {'codigo': 'B003', 'nombre': 'Banco Comercial', 'pais': 'España'},
            {'codigo': 'B004', 'nombre': 'Banco de Ahorros', 'pais': 'España'},
        ]
        
        bancos = []
        for banco_data in bancos_data:
            banco = Banco(**banco_data)
            bancos.append(banco)
            db.session.add(banco)
        
        db.session.commit()
        
        # Crear cuentas
        cuentas_data = [
            {'numero_cuenta': 'ES0012345678901234567890', 'banco_id': 1, 'titular': 'Juan Pérez', 'saldo': 10000.0},
            {'numero_cuenta': 'ES0012345678901234567891', 'banco_id': 1, 'titular': 'María García', 'saldo': 5000.0},
            {'numero_cuenta': 'ES0022345678901234567890', 'banco_id': 2, 'titular': 'Carlos López', 'saldo': 15000.0},
            {'numero_cuenta': 'ES0022345678901234567891', 'banco_id': 2, 'titular': 'Ana Martínez', 'saldo': 7500.0},
            {'numero_cuenta': 'ES0032345678901234567890', 'banco_id': 3, 'titular': 'Pedro Sánchez', 'saldo': 8000.0},
            {'numero_cuenta': 'ES0042345678901234567890', 'banco_id': 4, 'titular': 'Laura Fernández', 'saldo': 12000.0},
        ]
        
        for cuenta_data in cuentas_data:
            cuenta = Cuenta(**cuenta_data)
            db.session.add(cuenta)
        
        db.session.commit()
        
        print("✅ Base de datos inicializada correctamente")
        print(f"   - {len(bancos)} bancos creados")
        print(f"   - {len(cuentas_data)} cuentas creadas")

if __name__ == '__main__':
    inicializar_datos()
