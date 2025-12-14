from flask import Blueprint, request, jsonify
from extensions import db
from models.sensor import Sensor

sensor_bp = Blueprint('sensor', __name__)

# ==========================================
# 1. AMBIL SEMUA DATA SENSOR (GET)
# Dipakai di: Dashboard.jsx (useEffect)
# ==========================================
@sensor_bp.route('/sensors', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    # Ubah list object database menjadi list JSON
    output = [sensor.to_dict() for sensor in sensors]
    return jsonify(output), 200

# ==========================================
# 2. UPDATE STATUS ON/OFF (PUT)
# Dipakai di: Dashboard.jsx (handleTogglePower)
# ==========================================
@sensor_bp.route('/sensors/<int:id>/toggle', methods=['PUT'])
def toggle_sensor(id):
    sensor = Sensor.query.get(id)
    
    if not sensor:
        return jsonify({'message': 'Sensor tidak ditemukan'}), 404
        
    # Logika Toggle (kebalikan dari status sekarang)
    sensor.isOn = not sensor.isOn
    db.session.commit()
    
    return jsonify({
        'message': 'Status berhasil diubah',
        'sensor': sensor.to_dict()
    }), 200

# ==========================================
# 3. ISI DATA AWAL / RESET (POST)
# Gunakan ini SEKALI saja lewat Postman untuk mengisi data
# ==========================================
@sensor_bp.route('/sensors/seed', methods=['POST'])
def seed_sensors():
    # Hapus data lama (opsional, hati-hati)
    db.session.query(Sensor).delete()
    
    # Data awal sesuai Dashboard.jsx Anda
    initial_data = [
        Sensor(name='Sensor Sawah A1', status='online', value='85%', temp='28°C', humidity='72%', isOn=True),
        Sensor(name='Sensor Sawah A2', status='online', value='92%', temp='27°C', humidity='74%', isOn=True),
        Sensor(name='Sensor Sawah B1', status='offline', value='15%', temp=None, humidity=None, isOn=False),
        Sensor(name='Sensor Sawah B2', status='online', value='78%', temp='29°C', humidity='70%', isOn=False)
    ]
    
    db.session.add_all(initial_data)
    db.session.commit()
    
    return jsonify({'message': 'Database sensor berhasil diisi ulang!'}), 201