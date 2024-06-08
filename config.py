import os
import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

app = Flask(__name__)

# Генерация nonce для CSP
nonce = uuid.uuid4().hex

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notarial_acts.db'
app.config['SQLALCHEMY_BINDS'] = {
    'tariffs': 'sqlite:///tariffs.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Настройка параметров для безопасности
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

# Включение защиты CSRF
csrf = CSRFProtect(app)

migrate = Migrate(app, db)
