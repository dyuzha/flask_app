from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from urllib.parse import urlsplit
from datetime import datetime, timezone
"""
Представления - обработчики, которые отвечают на запросы веб-браузера,
Представления в Flask пишутся как Python функции.
Каждая функция представления сопоставляется с одним или несколькими URL
"""

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Страница редактирования профиля"""
    form = EditProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    # Если это GET запрос, значит пользователь еще не редактировал профиль
    # Поля заполняются текущими данными из бд
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    """Главная страница сайта"""
    posts = [ # список выдуманных постов
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = 'Home Page',
        posts = posts)


@app.route('/user/<username>')
@login_required
def user(username):
    """Страница пользователя"""
    # Если пользователь не существует - возвращает страницу 404
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [ {'author': user, 'body': 'Test post #1'},
             {'author': user, 'body': 'Test post #2'} ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Страница входа"""
    # Если пользователь зарегистрирован, то он перенаправляется на гл. страницу
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
                sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """Выход пользователя из системы и перенаправлеие на гл. страницу"""
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    """Выполняется перед каждым посещением любой страницы"""
    # Если пользователь авторизовае,
    if current_user.is_authenticated:
        # текущее время записывается в бд, как last_seen
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации пользователя"""
    # Если пользователь авторизован
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    # Если форма прошла валидацию
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
