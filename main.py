from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notarial_acts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Определение моделей
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    actions = db.relationship('Action', backref='category', lazy='dynamic')

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/notarial_acts")
def notarial_acts():
    return render_template('notarial_acts.html')

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
    app.run(debug=True)
