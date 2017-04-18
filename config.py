import os

class Config(object):
    # Определяет, включен ли режим отладки
    # В случае если включен, flask будет показывать
    # подробную отладочную информацию. Если выключен -
    # - 500 ошибку без какой либо дополнительной информации.
    DEBUG = False
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True
    # Случайный ключ, которые будет исползоваться для подписи
    # данных, например cookies.
    SECRET_KEY = ""
    basedir = os.path.abspath(os.path.dirname(__file__))
    secret_file = os.path.join(basedir, '.secret')
    if os.path.exists(secret_file):
        # Read SECRET_KEY from .secret file
        f = open(secret_file, 'r')
        SECRET_KEY = f.read().strip()
        f.close()
    else:
        # Generate SECRET_KEY & save it away
        SECRET_KEY = os.urandom(24)
        f = open(secret_file, 'w')
        f.write(str(SECRET_KEY))
        f.close()

    # URI используемая для подключения к базе данных
    pg_db_username = 'user'
    pg_db_password = 'password'
    pg_db_name = 'blog'
    pg_db_hostname = 'localhost'
    BLOGGING_DISQUS_SITENAME = 'test'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://'+pg_db_username+':'+pg_db_password+'@'+pg_db_hostname+'/'+pg_db_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADS_DEFAULT_DEST = '/static/img/'


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True