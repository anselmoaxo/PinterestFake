from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

#os.getenv('BD_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('BD_URL')
    #'postgresql://postgres:postgres@localhost/comunidade'
app.config['SECRET_KEY'] = "1813961736aa7f54661564ca5a8f06a6"
app.config['UPLOAD_FOLDER'] = "static/fotos_posts"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"
from fakepinterest import routes
