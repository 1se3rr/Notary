from flask_talisman import Talisman
from flask_wtf import CSRFProtect

from views import *
from admin import *


if __name__ == '__main__':
    app.run(debug=True)

