from config import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Category(db.Model):
    __tablename__ = 'categories'
    id_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    actions = db.relationship('NotaryAction', backref='category', lazy=True)

    def __str__(self):
        return self.name

class NotaryAction(db.Model):
    __tablename__ = 'notary_actions'
    id_action = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    description = db.Column(db.String(1000))

    def __str__(self):
        return self.name

class TariffType(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'id_tariff_types'
    id_tariff_types = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tariff_prices = db.relationship('TariffPrice', backref='tariff_type', lazy=True)

    def __str__(self):
        return self.name

class TariffPrice(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'tariff_prices'
    id_price = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    tariff_type_id = db.Column(db.Integer, db.ForeignKey('id_tariff_types.id_tariff_types'), nullable=False)
    id_service = db.Column(db.Integer, db.ForeignKey('services.id_service'), nullable=False)
    service = db.relationship('Service', backref='tariff_prices')

    def __str__(self):
        return f"{self.service.name} - {self.price}"

class ArticleNorm(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'article_norms'
    id_norm = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.name

class Title(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'titles'
    id_title = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    services = db.relationship('Service', backref='title', lazy=True)

    def __str__(self):
        return self.name

class Service(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'services'
    id_service = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title_id = db.Column(db.Integer, db.ForeignKey('titles.id_title'))
    norm_id = db.Column(db.Integer, db.ForeignKey('article_norms.id_norm'), nullable=False)
    article_norm = db.relationship('ArticleNorm', backref='services', lazy=True)

    def __str__(self):
        return self.name
