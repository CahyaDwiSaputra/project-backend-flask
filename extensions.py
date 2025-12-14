from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Inisialisasi plugin kosong
db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()