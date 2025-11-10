from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking_network.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Modelos
class Banco(db.Model):
    __tablename__ = 'bancos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(50), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    cuentas = db.relationship('Cuenta', backref='banco', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'pais': self.pais,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }

class Cuenta(db.Model):
    __tablename__ = 'cuentas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_cuenta = db.Column(db.String(20), unique=True, nullable=False)
    banco_id = db.Column(db.Integer, db.ForeignKey('bancos.id'), nullable=False)
    titular = db.Column(db.String(100), nullable=False)
    saldo = db.Column(db.Float, default=0.0, nullable=False)
    moneda = db.Column(db.String(3), default='USD', nullable=False)
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    transacciones_origen = db.relationship('Transaccion', 
                                          foreign_keys='Transaccion.cuenta_origen_id',
                                          backref='cuenta_origen', lazy=True)
    transacciones_destino = db.relationship('Transaccion',
                                           foreign_keys='Transaccion.cuenta_destino_id',
                                           backref='cuenta_destino', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_cuenta': self.numero_cuenta,
            'banco_id': self.banco_id,
            'banco_nombre': self.banco.nombre if self.banco else None,
            'titular': self.titular,
            'saldo': self.saldo,
            'moneda': self.moneda,
            'activa': self.activa,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }

class Transaccion(db.Model):
    __tablename__ = 'transacciones'
    
    id = db.Column(db.Integer, primary_key=True)
    cuenta_origen_id = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
    cuenta_destino_id = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    moneda = db.Column(db.String(3), default='USD', nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'transferencia', 'deposito', 'retiro'
    estado = db.Column(db.String(20), default='pendiente')  # 'pendiente', 'completada', 'rechazada'
    referencia = db.Column(db.String(50), unique=True)
    fecha_transaccion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_procesamiento = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cuenta_origen_id': self.cuenta_origen_id,
            'cuenta_origen_numero': self.cuenta_origen.numero_cuenta if self.cuenta_origen else None,
            'cuenta_destino_id': self.cuenta_destino_id,
            'cuenta_destino_numero': self.cuenta_destino.numero_cuenta if self.cuenta_destino else None,
            'monto': self.monto,
            'moneda': self.moneda,
            'tipo': self.tipo,
            'estado': self.estado,
            'referencia': self.referencia,
            'fecha_transaccion': self.fecha_transaccion.isoformat(),
            'fecha_procesamiento': self.fecha_procesamiento.isoformat() if self.fecha_procesamiento else None
        }

# Rutas API - Bancos
@app.route('/api/bancos', methods=['GET'])
def listar_bancos():
    bancos = Banco.query.filter_by(activo=True).all()
    return jsonify([banco.to_dict() for banco in bancos])

@app.route('/api/bancos', methods=['POST'])
def crear_banco():
    data = request.json
    banco = Banco(
        codigo=data['codigo'],
        nombre=data['nombre'],
        pais=data.get('pais', '')
    )
    db.session.add(banco)
    db.session.commit()
    return jsonify(banco.to_dict()), 201

@app.route('/api/bancos/<int:banco_id>', methods=['GET'])
def obtener_banco(banco_id):
    banco = Banco.query.get_or_404(banco_id)
    return jsonify(banco.to_dict())

# Rutas API - Cuentas
@app.route('/api/cuentas', methods=['GET'])
def listar_cuentas():
    banco_id = request.args.get('banco_id', type=int)
    query = Cuenta.query
    if banco_id:
        query = query.filter_by(banco_id=banco_id)
    cuentas = query.filter_by(activa=True).all()
    return jsonify([cuenta.to_dict() for cuenta in cuentas])

@app.route('/api/cuentas', methods=['POST'])
def crear_cuenta():
    data = request.json
    banco = Banco.query.get_or_404(data['banco_id'])
    
    cuenta = Cuenta(
        numero_cuenta=data['numero_cuenta'],
        banco_id=data['banco_id'],
        titular=data['titular'],
        saldo=data.get('saldo', 0.0),
        moneda=data.get('moneda', 'USD')
    )
    db.session.add(cuenta)
    db.session.commit()
    return jsonify(cuenta.to_dict()), 201

@app.route('/api/cuentas/<int:cuenta_id>', methods=['GET'])
def obtener_cuenta(cuenta_id):
    cuenta = Cuenta.query.get_or_404(cuenta_id)
    return jsonify(cuenta.to_dict())

@app.route('/api/cuentas/<int:cuenta_id>/saldo', methods=['GET'])
def obtener_saldo(cuenta_id):
    cuenta = Cuenta.query.get_or_404(cuenta_id)
    return jsonify({
        'numero_cuenta': cuenta.numero_cuenta,
        'saldo': cuenta.saldo,
        'moneda': cuenta.moneda
    })

# Rutas API - Transacciones
@app.route('/api/transacciones', methods=['GET'])
def listar_transacciones():
    cuenta_id = request.args.get('cuenta_id', type=int)
    query = Transaccion.query
    if cuenta_id:
        query = query.filter(
            (Transaccion.cuenta_origen_id == cuenta_id) |
            (Transaccion.cuenta_destino_id == cuenta_id)
        )
    transacciones = query.order_by(Transaccion.fecha_transaccion.desc()).limit(100).all()
    return jsonify([transaccion.to_dict() for transaccion in transacciones])

@app.route('/api/transacciones', methods=['POST'])
def crear_transaccion():
    data = request.json
    cuenta_origen = Cuenta.query.get_or_404(data['cuenta_origen_id'])
    cuenta_destino = Cuenta.query.get_or_404(data['cuenta_destino_id'])
    monto = float(data['monto'])
    
    # Validaciones
    if cuenta_origen.saldo < monto:
        return jsonify({'error': 'Saldo insuficiente'}), 400
    
    if cuenta_origen.moneda != cuenta_destino.moneda:
        return jsonify({'error': 'Las cuentas deben tener la misma moneda'}), 400
    
    if not cuenta_origen.activa or not cuenta_destino.activa:
        return jsonify({'error': 'Una o ambas cuentas están inactivas'}), 400
    
    # Crear transacción
    import uuid
    transaccion = Transaccion(
        cuenta_origen_id=cuenta_origen.id,
        cuenta_destino_id=cuenta_destino.id,
        monto=monto,
        moneda=cuenta_origen.moneda,
        tipo=data.get('tipo', 'transferencia'),
        referencia=data.get('referencia', str(uuid.uuid4()))
    )
    
    # Procesar transacción
    try:
        cuenta_origen.saldo -= monto
        cuenta_destino.saldo += monto
        transaccion.estado = 'completada'
        transaccion.fecha_procesamiento = datetime.utcnow()
        
        db.session.add(transaccion)
        db.session.commit()
        
        return jsonify(transaccion.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/transacciones/<int:transaccion_id>', methods=['GET'])
def obtener_transaccion(transaccion_id):
    transaccion = Transaccion.query.get_or_404(transaccion_id)
    return jsonify(transaccion.to_dict())

# Ruta para estadísticas de la red
@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    total_bancos = Banco.query.filter_by(activo=True).count()
    total_cuentas = Cuenta.query.filter_by(activa=True).count()
    total_transacciones = Transaccion.query.filter_by(estado='completada').count()
    volumen_total = db.session.query(db.func.sum(Transaccion.monto)).filter_by(estado='completada').scalar() or 0
    
    return jsonify({
        'total_bancos': total_bancos,
        'total_cuentas': total_cuentas,
        'total_transacciones': total_transacciones,
        'volumen_total_transacciones': float(volumen_total)
    })

# Inicializar base de datos
def crear_tablas():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    crear_tablas()
    app.run(debug=True, host='0.0.0.0', port=5000)
