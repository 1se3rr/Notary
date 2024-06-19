from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField

from flask_login import current_user, login_required, logout_user

from config import app, db
from models import Category, NotaryAction, TariffType, TariffPrice, Title, Service, ArticleNorm


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

    def on_model_change(self, form, model, is_created):
        """Обрабатывает данные из формы и записывает валидные данные"""
        model.category_id = form.data['category_id'].id_category


class TariffPriceView(MyModelView):
    form_columns = ['price', 'description', 'tariff_type_id', 'service']
    column_labels = dict(price='Цена', description='Описание', tariff_type_id='Тип тарифа', service='Услуга')

    def on_model_change(self, form, model, is_created):
        """Обрабатывает данные из формы и записывает валидные данные"""
        model.tariff_type_id = form.data['tariff_type_id'].id_tariff_types
        model.id_service = form.data['service'].id_service


class ServiceView(MyModelView):
    form_columns = ['name', 'title_id', 'norm_id']
    column_labels = dict(name='Наименование', title_id='Название', norm_id='Норма')

    def on_model_change(self, form, model, is_created):
        """Обрабатывает данные из формы и записывает валидные данные"""
        model.title_id = form.data['title_id'].id_title
        model.norm_id = form.data['norm_id'].id_norm


class MyAdminIndexView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        # Пример статистики
        category_count = Category.query.count()
        notary_action_count = NotaryAction.query.count()
        tariff_type_count = TariffType.query.count()
        tariff_price_count = TariffPrice.query.count()
        title_count = Title.query.count()
        service_count = Service.query.count()
        article_norm_count = ArticleNorm.query.count()

        # Передача данных в шаблон
        return self.render('admin/index.html', category_count=category_count,
                           notary_action_count=notary_action_count, tariff_type_count=tariff_type_count,
                           tariff_price_count=tariff_price_count, title_count=title_count,
                           service_count=service_count, article_norm_count=article_norm_count)


class logout(BaseView):
    @expose('/')
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('login'))


class DashBoard(AdminIndexView):
    @expose('/')
    def add_data_db(self):
        return self.render('admin/index.html, ')


admin = Admin(app, name='Админ Панель', template_mode='bootstrap3', index_view=MyAdminIndexView(), url='/admin_panel')
admin.add_view(logout(name='Выход'))

admin.add_view(MyModelView(Category, db.session, name='Категории'))
admin.add_view(NotaryActionView(NotaryAction, db.session, name='Нотариальные Действия'))
admin.add_view(MyModelView(TariffType, db.session, name='Типы Тарифов'))
admin.add_view(TariffPriceView(TariffPrice, db.session, name='Тарифы'))
admin.add_view(MyModelView(ArticleNorm, db.session, name='Нормы'))
admin.add_view(MyModelView(Title, db.session, name='Заголовки'))
admin.add_view(ServiceView(Service, db.session, name='Услуги'))
