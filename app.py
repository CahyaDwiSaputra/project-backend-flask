import time
from flask import Flask
from sqlalchemy.exc import OperationalError
from config import Config
from extensions import db, bcrypt, cors
from controllers.auth_controller import auth_bp
from controllers.sensor_controller import sensor_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(sensor_bp)
    
    # --- LOGIKA RETRY KONEKSI DATABASE ---
    with app.app_context():
        # Coba konek maksimal 10 kali
        for i in range(10):
            try:
                db.create_all()
                print("✅ Database Connected & Tables Created!")
                break # Berhasil, keluar dari loop
            except OperationalError as e:
                print(f"⚠️ Database belum siap... Retrying ({i+1}/10)")
                time.sleep(5) # Tunggu 5 detik sebelum coba lagi
        else:
            print("❌ Gagal konek ke Database setelah 10 percobaan.")
            # Tetap lanjut (atau bisa exit), tapi biasanya container akan restart
            
    return app

if __name__ == '__main__':
    app = create_app()
    # Host 0.0.0.0 PENTING agar bisa diakses dari luar container
    app.run(debug=True, host='0.0.0.0', port=5000)