from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField
from config import app, db
from models import Category, NotaryAction, TariffType, TariffPrice, Title, Service, ArticleNorm
from flask_login import current_user

class AdminMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyModelView(AdminMixin, ModelView):
    form_overrides = {
        'category_id': QuerySelectField,
        'tariff_type_id': QuerySelectField,
        'title_id': QuerySelectField,
        'norm_id': QuerySelectField
    }

    form_args = {
        'category_id': {
            'query_factory': lambda: Category.query,
            'get_label': 'name'
        },
        'tariff_type_id': {
            'query_factory': lambda: TariffType.query,
            'get_label': 'name'
        },
        'title_id': {
            'query_factory': lambda: Title.query,
            'get_label': 'name'
        },
        'norm_id': {
            'query_factory': lambda: ArticleNorm.query,
            'get_label': 'name'
        }
    }

class NotaryActionView(MyModelView):
    form_columns = ['name', 'category_id', 'description']
    column_labels = dict(name='Наименование', category_id='Категория', description='Описание')

class TariffPriceView(MyModelView):
    form_columns = ['price', 'description', 'tariff_type_id', 'service']
    column_labels = dict(price='Цена', description='Описание', tariff_type_id='Тип тарифа', service='Услуга')

class ServiceView(MyModelView):
    form_columns = ['name', 'title_id', 'norm_id']
    column_labels = dict(name='Наименование', title_id='Название', norm_id='Норма')



class MyAdminIndexView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin = Admin(app, name='Админ Панель', template_mode='bootstrap3', index_view=MyAdminIndexView(), url='/admin_panel')

admin.add_view(MyModelView(Category, db.session, name='Категории'))
admin.add_view(NotaryActionView(NotaryAction, db.session, name='Нотариальные Действия'))
admin.add_view(MyModelView(TariffType, db.session, name='Типы Тарифов'))
admin.add_view(TariffPriceView(TariffPrice, db.session, name='Тарифы'))
admin.add_view(MyModelView(ArticleNorm, db.session, name='Нормы'))
admin.add_view(MyModelView(Title, db.session, name='Заголовки'))
admin.add_view(ServiceView(Service, db.session, name='Услуги'))
