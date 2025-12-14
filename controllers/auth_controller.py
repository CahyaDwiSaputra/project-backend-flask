from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User

# Buat Blueprint (sekelompok rute)
auth_bp = Blueprint('auth', __name__)

# ==========================================
# REGISTER
# ==========================================
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Cek email
    user_exists = User.query.filter_by(email=data['email']).first()
    if user_exists:
        return jsonify(error='Email sudah terdaftar'), 409
        
    # Buat user baru
    # (Password di-hash otomatis di model User)
    new_user = User(
        fullName=data['fullName'],
        email=data['email'],
        phone=data['phone'],
        password=data['password']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(message='User berhasil dibuat'), 201

# ==========================================
# LOGIN
# ==========================================
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = User.query.filter_by(email=email).first()
    
    # Kita pakai method check_password dari model (lebih rapi)
    if user and user.check_password(password):
        return jsonify(
            message='Login berhasil', 
            user={
                'fullName': user.fullName, 
                'email': user.email, 
                'phone': user.phone, 
                'role': user.role
            }
        ), 200
    else:
        return jsonify(error='Email atau password salah'), 401