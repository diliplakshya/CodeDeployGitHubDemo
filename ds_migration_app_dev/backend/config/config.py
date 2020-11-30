"""
Flask config.

FLASK_ENV:
	The environment the app is running in, such as development or production.
	Setting the environment to development mode will automatically trigger other variables,
	such as setting DEBUG to True.
	Flask plugins similarly behave differently when this is true.

DEBUG:
	Extremely useful when developing! DEBUG mode triggers several things.
	Exceptions thrown by the app will print to console automatically,
	app crashes will result in a helpful error screen,
	and your app will auto-reload when changes are detected.

TESTING:
	This mode ensures exceptions are propagated rather than
	handled by the app's error handlers, which is useful when running automated tests.

SECRET_KEY:
	Flask "secret keys" are random strings used to
	encrypt sensitive user data, such as passwords. Encrypting data in Flask
	depends on the randomness of this string, which means decrypting the same
	data is as simple as getting a hold of this string's value.
	Guard your secret key with your life; ideally,
	even you shouldn't know the value of this variable.

SERVER_NAME:
	If you intend your app to be reachable on a custom domain,
	we specify the app's domain name here.

"""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    DB_SERVER = environ.get('DB_SERVER')

    @property
    def DATABASE_URI(self):  # Note: all caps
        return ''.format(self.DB_SERVER)


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

    DATABASE_URI = environ.get('DATABASE_DEV_URI')
    CASSANDRA_HOSTS = environ.get('CASSANDRA_HOSTS_DEV')
    CASSANDRA_KEYSPACE = environ.get('CASSANDRA_KEYSPACE_DEV')

    # Database
    CSQLALCHEMY_DATABASE_URI = environ.get('CSQLALCHEMY_DATABASE_DEV_URI')

    # AWS Secrets
    AWS_KEY_ID_DEV = environ.get('AWS_KEY_ID_DEV')
    AWS_SECRET_KEY_DEV = environ.get('AWS_ACCESS_KEY_DEV')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    DATABASE_URI = environ.get('DATABASE_PROD_URI')
    CASSANDRA_HOSTS = environ.get('CASSANDRA_HOSTS_PROD')
    CASSANDRA_KEYSPACE = environ.get('CASSANDRA_KEYSPACE_PROD')

    # Database
    CSQLALCHEMY_DATABASE_URI = environ.get('CSQLALCHEMY_DATABASE_PROD_URI')

    # AWS Secrets
    AWS_KEY_ID_DEV = environ.get('AWS_KEY_ID_PROD')
    AWS_SECRET_KEY_DEV = environ.get('AWS_ACCESS_KEY_PROD')
