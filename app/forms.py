from flask import Flask, render_template, redirect, url_for, flash, request
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User  # Импортируем модель пользователя
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Страница игры
@app.route('/game')
@login_required
def game():
    return render_template('game.html', clicks=current_user.clicks)


# Обработка кликов
@app.route('/click', methods=['POST'])
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('game'))


# Вход в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('game'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')

    return render_template('login.html')


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Это имя пользователя уже занято!', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Аккаунт успешно создан! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)