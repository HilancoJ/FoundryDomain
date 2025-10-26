from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
	DB_DIR = create_database_directory()
	DB_NAME = "finances.db"
	DB_PATH = DB_DIR + '/' + DB_NAME

	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'encryption key'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	from .views import views
	from .auth import auth
	app.register_blueprint(views,url_prefix='/')
	app.register_blueprint(auth,url_prefix='/')

	from .models import User, Note
	create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app


def create_database_directory():
	DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'database'))
	if not os.path.exists(DB_DIR):
		os.mkdir(DB_DIR)
		print('Created database directory!')
	else:
		print('Database directory already exists.')
	return DB_DIR


def create_database(app):
	if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'][10:len(app.config['SQLALCHEMY_DATABASE_URI'])]):
		db.create_all(app=app)
		print('Created database!')
	else:
		print('Database already exists.')