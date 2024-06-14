from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from config import app, db
from models import AdminUser, Category, NotaryAction, TariffType, TariffPrice, Title, Service, ArticleNorm
from forms import LoginForm


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('Неверное имя пользователя или пароль')
    return render_template('admin/login.html', form=form)


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


@app.route('/admin_panel')
@login_required
def admin_panel():
    return redirect(url_for('admin.index'))
