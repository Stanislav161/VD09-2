from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin  # Импортирован UserMixin
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ваш_секретный_ключ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clicker.db'
db = SQLAlchemy(app)
# Инициализация LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Указываем имя функции представления для входа
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    clicks = db.Column(db.Integer, default=0)  # Поле для хранения кликов
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))