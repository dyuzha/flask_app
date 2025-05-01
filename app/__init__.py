from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

def run_mail_logger():
    """Запускает режим отладки по электронной почте"""
    # Если указаны параметры авторизации, исопльзует авторизацию
    if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    else:
        auth = None

    # Если параметр шифрования - True, использует шифрование
    if app.config['MAIL_USE_TLS']:
        secure = ()
    else:
        secure = None

    # Создание обработчика
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'],
        subject='Microblog Failure', # Тема письма
        credentials=auth, secure=secure)

    # Подключение к логеру фласк
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

def run_journal_log():
    # Создает папку logs, елси она не найдена
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)

    # Подключение к логеру фласк
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Falsk_app startup')


# Если запущен в продакшене
if not app.debug:
    run_journal_log()

    # Если есть конфигурация сервера
    if app.config['MAIL_SERVER']:
        run_mail_logger()

from app import routes, models, errors
