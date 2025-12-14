import os

class Config:
    # Settingan Database (Sesuai docker-compose Anda)
    # Jika dijalankan di Docker: host='mysql_db'
    # Jika dijalankan manual tanpa docker: host='localhost'
    
    # Kita pakai logika: Cek dulu apakah ada variabel environment, kalau tidak pakai default
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@mysql_db/rawattani_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False