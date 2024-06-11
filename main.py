from flask_talisman import Talisman
from flask_wtf import CSRFProtect

from views import *
from admin import *

csrf = CSRFProtect(app)

csp = {
    'default-src': ["'self'"],
    'script-src': ["'report-sample'", "'self'"],
    'style-src': ["'report-sample'", "'self'"],
    'object-src': ["'none'"],
    'base-uri': ["'self'"],
    'connect-src': ["'self'"],
    'font-src': ["'self'"],
    'frame-src': ["'self'"],
    'img-src': ["'self'"],
    'manifest-src': ["'self'"],
    'media-src': ["'self'"],
    'report-uri': ['https://6666ef9dd528e3ceb6b0c68a.endpoint.csper.io/?v=2'],
    'worker-src': ["'none'"],
    'frame-ancestors': ["'self'"],
    'form-action': ["'self'"]
}

# Дополнительные заголовки безопасности
talisman = Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src', 'style-src'],
    frame_options='DENY',
    strict_transport_security=True,
    strict_transport_security_preload=True,
    strict_transport_security_max_age=31536000,
    strict_transport_security_include_subdomains=True,
    x_content_type_options=True,
    x_xss_protection=True
)

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
