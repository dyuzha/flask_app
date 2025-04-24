import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    CSRF_ENABLED = True
    SECRET_KEY = SECRET_KEY = os.environ.get('SECRET_KEY') or \
            'you-will-never-guess'
    # Путь к файлу с бд
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Директория с миграционными файлами
    # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
