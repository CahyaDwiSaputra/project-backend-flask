from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Inisialisasi Aplikasi
app = Flask(__name__)
CORS(app) # Izinkan React (dari port 3000) mengakses Flask (di port 5000)

# =======================================================
# KONEKSI KE DATABASE (SESUAIKAN DENGAN PUNYA ANDA)
# =======================================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/rawattani_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# =======================================================
# MODEL DATABASE (DISESUAIKAN DENGAN REGISTER.JSX)
# =======================================================
class User(db.Model):
    # Nama tabel di database
    __tablename__ = 'user' 
    
    # Kolom-kolomnya, SESUAIKAN DENGAN PHP MYADMIN
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    # Fungsi untuk membuat objek User baru
    def __init__(self, fullName, email, phone, password):
        self.fullName = fullName
        self.email = email
        self.phone = phone
        # Password langsung di-hash saat dibuat
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

# Buat tabel jika belum ada
with app.app_context():
    db.create_all()

# =======================================================
# ENDPOINT API UNTUK REGISTER (SESUAI REGISTER.JSX)
# =======================================================
@app.route('/register', methods=['POST'])
def register():
    # Ambil data JSON yang dikirim oleh React
    data = request.get_json()
    
    # Cek apakah email sudah terdaftar
    user_exists = User.query.filter_by(email=data['email']).first()
    if user_exists:
        return jsonify(error='Email sudah terdaftar'), 409 # 409 = Conflict
        
    # Buat user baru dengan semua data
    new_user = User(
        fullName=data['fullName'],
        email=data['email'],
        phone=data['phone'],
        password=data['password']
    )
    
    # Simpan ke database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(message='User berhasil dibuat'), 201 # 201 = Created

# =======================================================
# ENDPOINT API UNTUK LOGIN (SESUAI LOGIN.JSX)
# =======================================================
@app.route('/login', methods=['POST'])
def login():
    # Ambil data JSON dari React
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    # Cari user di database berdasarkan email
    user = User.query.filter_by(email=email).first()
    
    # Cek user dan password (hash)
    if user and bcrypt.check_password_hash(user.password, password):
        # Jika berhasil, kirim pesan dan nama user
        return jsonify(
            message='Login berhasil', 
            user={'fullName': user.fullName, 'email': user.email, 'phone': user.phone, 'role': user.role}
        ), 200
    else:
        # Jika gagal
        return jsonify(error='Email atau password salah'), 401 # 401 = Unauthorized

# =======================================================
# JALANKAN SERVER
# =======================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)