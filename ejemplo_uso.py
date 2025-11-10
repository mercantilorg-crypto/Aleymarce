"""
Ejemplo de uso de la API de Red Bancaria
Ejecutar este script después de iniciar el servidor Flask (python app.py)
"""
import requests
import json

BASE_URL = 'http://localhost:5000/api'

def ejemplo_completo():
    print("=" * 60)
    print("EJEMPLO DE USO DE LA RED BANCARIA")
    print("=" * 60)
    
    # 1. Listar bancos
    print("\n1. Listando bancos disponibles...")
    response = requests.get(f'{BASE_URL}/bancos')
    bancos = response.json()
    print(f"   Encontrados {len(bancos)} bancos:")
    for banco in bancos:
        print(f"   - {banco['nombre']} ({banco['codigo']})")
    
    # 2. Listar cuentas
    print("\n2. Listando cuentas disponibles...")
    response = requests.get(f'{BASE_URL}/cuentas')
    cuentas = response.json()
    print(f"   Encontradas {len(cuentas)} cuentas:")
    for cuenta in cuentas[:3]:  # Mostrar solo las primeras 3
        print(f"   - {cuenta['numero_cuenta']}: {cuenta['titular']} (Saldo: {cuenta['saldo']} {cuenta['moneda']})")
    
    # 3. Obtener saldo de una cuenta
    if cuentas:
        cuenta_id = cuentas[0]['id']
        print(f"\n3. Obteniendo saldo de la cuenta {cuenta_id}...")
        response = requests.get(f'{BASE_URL}/cuentas/{cuenta_id}/saldo')
        saldo = response.json()
        print(f"   Saldo: {saldo['saldo']} {saldo['moneda']}")
    
    # 4. Realizar una transferencia
    if len(cuentas) >= 2:
        cuenta_origen = cuentas[0]
        cuenta_destino = cuentas[1]
        monto = 100.0
        
        print(f"\n4. Realizando transferencia de {monto} {cuenta_origen['moneda']}...")
        print(f"   De: {cuenta_origen['titular']} ({cuenta_origen['numero_cuenta']})")
        print(f"   A: {cuenta_destino['titular']} ({cuenta_destino['numero_cuenta']})")
        
        transaccion_data = {
            'cuenta_origen_id': cuenta_origen['id'],
            'cuenta_destino_id': cuenta_destino['id'],
            'monto': monto,
            'tipo': 'transferencia'
        }
        
        response = requests.post(
            f'{BASE_URL}/transacciones',
            json=transaccion_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            transaccion = response.json()
            print(f"   ✅ Transferencia completada!")
            print(f"   Referencia: {transaccion['referencia']}")
            print(f"   Estado: {transaccion['estado']}")
        else:
            print(f"   ❌ Error: {response.json()}")
    
    # 5. Listar transacciones recientes
    print("\n5. Listando transacciones recientes...")
    response = requests.get(f'{BASE_URL}/transacciones')
    transacciones = response.json()
    print(f"   Encontradas {len(transacciones)} transacciones:")
    for trans in transacciones[:3]:  # Mostrar solo las primeras 3
        print(f"   - {trans['tipo']}: {trans['monto']} {trans['moneda']} (Estado: {trans['estado']})")
    
    # 6. Obtener estadísticas
    print("\n6. Obteniendo estadísticas de la red...")
    response = requests.get(f'{BASE_URL}/estadisticas')
    stats = response.json()
    print(f"   Total de bancos: {stats['total_bancos']}")
    print(f"   Total de cuentas: {stats['total_cuentas']}")
    print(f"   Total de transacciones: {stats['total_transacciones']}")
    print(f"   Volumen total: {stats['volumen_total_transacciones']}")
    
    print("\n" + "=" * 60)
    print("EJEMPLO COMPLETADO")
    print("=" * 60)

if __name__ == '__main__':
    try:
        ejemplo_completo()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor.")
        print("   Asegúrate de que el servidor Flask esté ejecutándose:")
        print("   python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
