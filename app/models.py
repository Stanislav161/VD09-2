from app import db
from app import login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):  # Исправлено: db.model на db.Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    clicks = db.Column(db.Integer, default=0)  # Исправлено: defaults на default

    def __repr__(self):  # Исправлено: repr на __repr__
        return f'User {self.username} - clicks: {self.clicks}'  # Исправлено: добавлены кавычки и исправлен синтаксис


@login_manager.user_loader  # Этот декоратор связывает функцию с flask_login, чтобы загружать пользователя по id
def load_user(user_id):
    return User.query.get(int(user_id))
