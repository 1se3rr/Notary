
from views import *
from admin import *

#

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
