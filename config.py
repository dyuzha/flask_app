import os

class Config:
    CSRF_ENABLED = True
    SECRET_KEY = SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'you-will-never-guess'

    OPENID_PROVIDERS = [
        { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
        { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
        { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
        { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
        { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Путь к файлу с бд
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Директория с миграционными файлами
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
