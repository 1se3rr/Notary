from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notarial_acts.db'
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
    app.run(debug=True)
