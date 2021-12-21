from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from exts import db
from apps import create_app
from apps.bluelog.models import Admin, Category, Post, Comment, Link

app = create_app()
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
