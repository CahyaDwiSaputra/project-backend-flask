from extensions import db, bcrypt

class User(db.Model):
    __tablename__ = 'user' 
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    def __init__(self, fullName, email, phone, password):
        self.fullName = fullName
        self.email = email
        self.phone = phone
        # Hash password saat inisialisasi
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Opsional: Fungsi helper untuk mengecek password
    def check_password(self, password_input):
        return bcrypt.check_password_hash(self.password, password_input)