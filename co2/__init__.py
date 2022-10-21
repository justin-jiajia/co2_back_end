from os import getenv
from apiflask import APIFlask
from datetime import datetime, timedelta
from click import option, confirm, echo
from .extensions import db, cors
from .api.v1 import api_v1
from .settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = getenv('FLASK_CONFIG', 'development')
    app = APIFlask('co2', 'Co2', 'v1.0')
    app.config.from_object(config[config_name])
    register_app(app)
    register_extensions(app)
    register_commands(app)
    register_blueprints(app)
    return app


def register_app(app):
    app.config[
        'SWAGGER_UI_CSS'] = 'https://lf26-cdn-tos.bytecdntp.com/cdn/expire-1-M/swagger-ui/4.5.2/swagger-ui.min.css'
    app.config['SWAGGER_UI_BUNDLE_JS'] = 'https://lf6-cdn-tos.bytecdntp.com/cdn/expire-1-M/swagger-ui/4.5.2/swagger' \
                                         '-ui-bundle.min.js '
    app.config['SWAGGER_UI_STANDALONE_PRESET_JS'] = 'https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/swagger-ui/4.5' \
                                                    '.2/swagger-ui-standalone-preset.min.js '


def register_commands(app):
    @app.cli.command()
    @option('--drop', is_flag=True, help='Create after drop.')
    def init_db(drop):
        """Initialize the database."""
        if drop:
            confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            echo('Drop tables.')
        db.create_all()
        echo('Initialized database.')

    @app.cli.command()
    def d_day_log():
        from .models import User, Log, DayLog
        time_now = datetime.now()
        for user in User.query.all():
            today_pf = 0
            for log in Log.query.filter(Log.author == user) \
                    .filter(Log.timestamp >= time_now - timedelta(days=1)).all():
                today_pf += log.co2_l
            today_pf = -today_pf
            if today_pf < 0:
                today_pf = 0
            user.jf += int(today_pf / 2)
            user.jf_yesterday = int(today_pf / 2)
        db.session.commit()


def register_extensions(app):
    db.init_app(app)
    cors.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api_v1, url_prefix='/api_v1/')
