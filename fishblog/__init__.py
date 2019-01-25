import os
import click
from flask import Flask, render_template

from fishblog.blueprints.admin import admin_bp
from fishblog.blueprints.auth import auth_bp
from fishblog.blueprints.blog import blog_bp
from fishblog.settings import config
from fishblog.extensions import bootstrap, db, ckeditor, mail, moment


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('fishblog')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_tmplate_context(app)
    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix='admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_tmplate_context(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10')
    @click.option('--post', default=50, help='Quantity of post, default is 50')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500')
    def forge(category, post, comment):
        """Generates the fake categories, posts, comments."""
        from fishblog.faker import fake_admin, fake_categories, fake_comments, fake_posts

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories()

        click.echo('Generating %d posts...' % post)
        fake_posts()

        click.echo('Generating %d comments...' % comment)
        fake_comments()

        click.echo('Done.')
