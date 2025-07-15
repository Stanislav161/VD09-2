from flask import Flask, render_template, redirect, url_for, flash
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user

# Добавляем маршруты
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Временная заглушка - замените реальной логикой
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/game')
@login_required
def game():
    return "Страница игры - требуется авторизация"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)