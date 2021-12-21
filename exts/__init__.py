from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_wtf import CSRFProtect



db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    from apps.bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user
