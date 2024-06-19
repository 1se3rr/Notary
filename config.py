import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

app = Flask(__name__)

# Генерация nonce для CSP
nonce = os.urandom(16).hex()

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/notarial_acts'
app.config['SQLALCHEMY_BINDS'] = {
    'tariffs': 'mysql+pymysql://root:root@localhost/tariffs',
    'admin': 'mysql+pymysql://root:root@localhost/admin_profile'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

# Включение защиты CSRF
csrf = CSRFProtect(app)

migrate = Migrate(app, db)
