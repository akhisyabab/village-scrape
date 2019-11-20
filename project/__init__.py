import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# instantiate the extensions
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app(script_info=None):
    from project.models import models
    from project.api.users import UserRegistration, UserLogin, UserLogoutAccess, UserLogoutRefresh, TokenRefresh, \
        AllUsers, SecretResource, UserProfile, UserEdit, AddAdmin

    from project.admin.views import admin_blueprint
    from project.scraper.views import scraper_blueprint

    # instantiate the app
    app = Flask(__name__, static_url_path='')

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    app.config['JWT_SECRET_KEY'] = 'village-scraper-jwt-key'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Setting up flask login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "admin.login"
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.filter(models.User.id == int(user_id)).first()


    jwt = JWTManager(app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return models.RevokedToken.is_jti_blacklisted(jti)

    # register blueprints or api resource
    api = Api(app, prefix="/api/v1")

    # Users
    api.add_resource(UserRegistration, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogoutAccess, '/logout/access')
    api.add_resource(UserLogoutRefresh, '/logout/refresh')
    api.add_resource(TokenRefresh, '/token/refresh')
    api.add_resource(AllUsers, '/users')
    api.add_resource(SecretResource, '/secret')
    api.add_resource(UserProfile, '/user/profile')
    api.add_resource(UserEdit, '/user/edit')
    api.add_resource(AddAdmin, '/admin/add')

    # register the blueprints
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(scraper_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
