from extensions import db

class Sensor(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='offline') # 'online' atau 'offline'
    
    # Kita pakai String dulu agar sama persis dengan React Anda ("85%", "28°C")
    # Nanti kalau sudah ada alat IoT beneran, bisa diubah jadi Float/Integer
    value = db.Column(db.String(20), nullable=True) 
    temp = db.Column(db.String(20), nullable=True)
    humidity = db.Column(db.String(20), nullable=True)
    
    isOn = db.Column(db.Boolean, default=False)

    def __init__(self, name, status, value, temp, humidity, isOn):
        self.name = name
        self.status = status
        self.value = value
        self.temp = temp
        self.humidity = humidity
        self.isOn = isOn

    # Helper untuk mengubah object database jadi JSON (Dictionary)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'value': self.value,
            'temp': self.temp,
            'humidity': self.humidity,
            'isOn': self.isOn
        }