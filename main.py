from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Конфигурация первой базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notarial_acts.db'
app.config['SQLALCHEMY_BINDS'] = {
    'tariffs': 'sqlite:///tariffs.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    actions = db.relationship('Action', backref='category', lazy=True)


class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
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


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/notarial_acts')
def notarial_acts():
    categories = Category.query.all()
    categories_data = [{
        'id': category.id,
        'name': category.name,
        'actions': [{'name': action.name, 'description': action.description} for action in category.actions]
    } for category in categories]
    return render_template('notarial_acts.html', categories=categories_data)


@app.route('/api/categories')
def categories_api():
    categories = Category.query.all()
    categories_data = [{
        'id': category.id,
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


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/admin/notarial_acts", methods=["GET", "POST"])
def admin_notarial_acts():
    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "add_category":
            name = request.form.get("name")
            new_category = Category(name=name)
            db.session.add(new_category)
            db.session.commit()
        elif form_type == "edit_category":
            id = request.form.get("id")
            name = request.form.get("name")
            category = db.session.get(Category, id)
            if category:
                category.name = name
                db.session.commit()
        elif form_type == "delete_category":
            id = request.form.get("id")
            category = db.session.get(Category, id)
            if category:
                db.session.delete(category)
                db.session.commit()
        elif form_type == "add_action":
            name = request.form.get("name")
            description = request.form.get("description")
            category_id = request.form.get("category_id")
            new_action = Action(name=name, description=description, category_id=category_id)
            db.session.add(new_action)
            db.session.commit()
        elif form_type == "edit_action":
            id = request.form.get("id")
            name = request.form.get("name")
            description = request.form.get("description")
            category_id = request.form.get("category_id")
            action = db.session.get(Action, id)
            if action:
                action.name = name
                action.description = description
                action.category_id = category_id
                db.session.commit()
        elif form_type == "delete_action":
            id = request.form.get("id")
            action = db.session.get(Action, id)
            if action:
                db.session.delete(action)
                db.session.commit()

    categories = Category.query.all()
    actions = Action.query.all()
    return render_template('admin_notarial_acts.html', categories=categories, actions=actions)


@app.route("/admin/tariffs", methods=["GET", "POST"])
def admin_tariffs():
    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "add_title":
            name = request.form.get("name")
            new_title = Title(name=name)
            db.session.add(new_title)
            db.session.commit()
        elif form_type == "edit_title":
            id = request.form.get("id")
            name = request.form.get("name")
            title = db.session.get(Title, id)
            if title:
                title.name = name
                db.session.commit()
        elif form_type == "delete_title":
            id = request.form.get("id")
            title = db.session.get(Title, id)
            if title:
                db.session.delete(title)
                db.session.commit()
        elif form_type == "add_norm":
            name = request.form.get("name")
            new_norm = ArticleNorm(name=name)
            db.session.add(new_norm)
            db.session.commit()
        elif form_type == "edit_norm":
            id = request.form.get("id")
            name = request.form.get("name")
            norm = db.session.get(ArticleNorm, id)
            if norm:
                norm.name = name
                db.session.commit()
        elif form_type == "delete_norm":
            id = request.form.get("id")
            norm = db.session.get(ArticleNorm, id)
            if norm:
                db.session.delete(norm)
                db.session.commit()
        elif form_type == "add_tariff_type":
            name = request.form.get("name")
            new_tariff_type = TariffType(name=name)
            db.session.add(new_tariff_type)
            db.session.commit()
        elif form_type == "edit_tariff_type":
            id = request.form.get("id")
            name = request.form.get("name")
            tariff_type = db.session.get(TariffType, id)
            if tariff_type:
                tariff_type.name = name
                db.session.commit()
        elif form_type == "delete_tariff_type":
            id = request.form.get("id")
            tariff_type = db.session.get(TariffType, id)
            if tariff_type:
                db.session.delete(tariff_type)
                db.session.commit()
        elif form_type == "add_service":
            name = request.form.get("name")
            title_id = request.form.get("title_id")
            norm_id = request.form.get("norm_id")
            new_service = Service(name=name, title_id=title_id, norm_id=norm_id)
            db.session.add(new_service)
            db.session.commit()
        elif form_type == "edit_service":
            id = request.form.get("id")
            name = request.form.get("name")
            title_id = request.form.get("title_id")
            norm_id = request.form.get("norm_id")
            service = db.session.get(Service, id)
            if service:
                service.name = name
                service.title_id = title_id
                service.norm_id = norm_id
                db.session.commit()
        elif form_type == "delete_service":
            id = request.form.get("id")
            service = db.session.get(Service, id)
            if service:
                db.session.delete(service)
                db.session.commit()
        elif form_type == "add_tariff":
            price = float(request.form.get("price").replace(",", "."))
            description = request.form.get("description")
            tariff_type_id = request.form.get("tariff_type_id")
            service_id = request.form.get("service_id")
            new_tariff = TariffPrice(price=price, description=description, tariff_type_id=tariff_type_id, id_service=service_id)
            db.session.add(new_tariff)
            db.session.commit()
        elif form_type == "edit_tariff":
            id = request.form.get("id")
            price = float(request.form.get("price").replace(",", "."))
            description = request.form.get("description")
            tariff_type_id = request.form.get("tariff_type_id")
            service_id = request.form.get("service_id")
            tariff = db.session.get(TariffPrice, id)
            if tariff:
                tariff.price = price
                tariff.description = description
                tariff.tariff_type_id = tariff_type_id
                tariff.id_service = service_id
                db.session.commit()
        elif form_type == "delete_tariff":
            id = request.form.get("id")
            tariff = db.session.get(TariffPrice, id)
            if tariff:
                db.session.delete(tariff)
                db.session.commit()

    titles = Title.query.all()
    norms = ArticleNorm.query.all()
    tariff_types = TariffType.query.all()
    services = Service.query.all()
    tariffs = TariffPrice.query.all()
    return render_template('admin_tariffs.html', titles=titles, norms=norms, tariff_types=tariff_types, services=services, tariffs=tariffs)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создать все таблицы базы данных в контексте приложения
    app.run(debug=True)
