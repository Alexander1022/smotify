from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
import datetime

UPLOAD_FOLDER = './app/static/uploads'
ONLY_ALLOWED = {'mp3', 'wav', 'ogg', 'wma'}
GENRES = {'rock', 'pop', 'hiphop', 'house', 'trap', 'chill', 'popfolk', 'metal', 'classical', 'kpop', 'polka', 'reggae', 'punk', 'funk', 'country'}
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.permanent_session_lifetime = datetime.timedelta(days=365)
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from app import routes

