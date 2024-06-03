import uuid

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_talisman import Talisman

app = Flask(__name__)

# Генерация nonce для CSP
nonce = uuid.uuid4().hex

# Обновленная конфигурация CSP


# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notarial_acts.db'
app.config['SQLALCHEMY_BINDS'] = {
    'tariffs': 'sqlite:///tariffs.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)


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


class NotaryAction(db.Model):
    __tablename__ = 'notary_actions'
    id_action = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    description = db.Column(db.String(255))


class TariffType(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'id_tariff_types'
    id_tariff_types = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tariff_prices = db.relationship('TariffPrice', backref='tariff_type', lazy=True)


class TariffPrice(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'tariff_prices'
    id_price = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    tariff_type_id = db.Column(db.Integer, db.ForeignKey('id_tariff_types.id_tariff_types'), nullable=False)
    id_service = db.Column(db.Integer, db.ForeignKey('services.id_service'), nullable=False)
    service = db.relationship('Service', backref='tariff_prices')


class ArticleNorm(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'article_norms'
    id_norm = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Title(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'titles'
    id_title = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    services = db.relationship('Service', backref='title', lazy=True)


class Service(db.Model):
    __bind_key__ = 'tariffs'
    __tablename__ = 'services'
    id_service = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title_id = db.Column(db.Integer, db.ForeignKey('titles.id_title'))
    norm_id = db.Column(db.Integer, db.ForeignKey('article_norms.id_norm'), nullable=False)
    article_norm = db.relationship('ArticleNorm', backref='services', lazy=True)


# Настройка админской панели с защитой
class AdminMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class MyModelView(AdminMixin, ModelView):
    pass


class MyAdminIndexView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app, name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView(), url='/admin_panel')

# Создаем движки и сессии для каждой базы данных
with app.app_context():
    notarial_engine = db.engine
    tariffs_engine = db.engines['tariffs']

    NotarialActsSession = sessionmaker(bind=notarial_engine)
    TariffsSession = sessionmaker(bind=tariffs_engine)

    notarial_session = NotarialActsSession()
    tariffs_session = TariffsSession()

    # Добавляем модели в Flask-Admin
    admin.add_view(MyModelView(Category, db.session))
    admin.add_view(MyModelView(NotaryAction, db.session))
    admin.add_view(MyModelView(TariffType, tariffs_session))
    admin.add_view(MyModelView(TariffPrice, tariffs_session))
    admin.add_view(MyModelView(ArticleNorm, tariffs_session))
    admin.add_view(MyModelView(Title, tariffs_session))
    admin.add_view(MyModelView(Service, tariffs_session))


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/notarial_acts')
def notarial_acts():
    categories = Category.query.all()
    categories_data = [{
        'id': category.id_category,
        'name': category.name,
        'actions': [{'name': action.name, 'description': action.description} for action in category.actions]
    } for category in categories]
    return render_template('notarial_acts.html', categories=categories_data)


@app.route('/api/categories')
def categories_api():
    categories = Category.query.all()
    categories_data = [{
        'id': category.id_category,
        'name': category.name,
        'actions': [{'name': action.name, 'description': action.description} for action in category.actions]
    } for category in categories]
    return jsonify(categories_data)


@app.route('/api/tariffs')
def tariffs_api():
    titles = Title.query.all()
    tariffs_data = [{
        'title': title.name,
        'services': [{
            'name': service.name,
            'norm': service.article_norm.name if service.article_norm else '',
            'tariffs': [{
                'type': price.tariff_type.name,
                'price': price.price,
                'description': price.description
            } for price in service.tariff_prices]
        } for service in title.services]
    } for title in titles]

    return jsonify(tariffs_data)


@app.route("/tariffs")
def tariffs():
    return render_template('tariffs.html')


@app.route("/about_us")
def about_us():
    return render_template('about_us.html')


@app.route("/contact_us")
def contact_us():
    return render_template('contact_us.html')


@app.route("/FAQ")
def FAQ():
    return render_template('FAQ.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создать все таблицы базы данных в контексте приложения
        # Создание администратора по умолчанию (если необходимо)
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin')
            admin_user.set_password('Qaz123Qwe')
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)
