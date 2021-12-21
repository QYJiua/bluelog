import click

from flask import Flask

from settings import DevelopmentConfig
from exts import db, login_manager, csrf
from apps.bluelog.views import bluelog_bp
from fakes import fake_admin, fake_category, fake_posts, fake_comments, fake_links


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    register_blueprints(app)
    register_extensions(app)
    register_command(app)
    return app


def register_blueprints(app):
    app.register_blueprint(bluelog_bp)


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_command(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""


        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_category(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')



